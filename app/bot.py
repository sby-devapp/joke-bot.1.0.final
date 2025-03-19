from telegram import Update
from telegram.ext import ContextTypes
import random


class JokeBot:
    def __init__(self, jokes_db):
        self.jokes_db = jokes_db
        self.SUPPORTED_LANGUAGES = self.jokes_db.get_supported_languages()  # Dynamically fetch supported languages

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        chat_type = update.message.chat.type
        print(f"[LOG] /start executed | Chat ID: {chat_id} | Type: {chat_type}")

        if chat_type in ['group', 'supergroup']:
            # Check if the user is an admin in group chats
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_ids = [admin.user.id for admin in admins]
            if update.message.from_user.id not in admin_ids:
                await update.message.reply_text("Only admins can start the bot in this group.")
                return

            # Add the chat to active_chats with default language 'en' and schedule 300 seconds (5 minutes)
            self.jokes_db.add_active_chat(chat_id, preferred_language='en', schedule=300)
            await update.message.reply_text("Starting to send random jokes to the group!")
            self.schedule_random_jokes(context.job_queue, chat_id)
        else:
            # Private chat: Add the chat to active_chats but do not schedule jokes
            self.jokes_db.add_active_chat(chat_id, preferred_language='en', schedule=None)
            joke, joke_id = self.jokes_db.get_random_joke_with_id('en')  # Send one joke as a greeting
            await update.message.reply_text(
                f"Hi! I'm the Joke Bot. Here's a joke for you:\n\n{joke}\n\nType /help for more info!"
            )
            print(f"[LOG] Sent initial joke | Chat ID: {chat_id} | Joke ID: {joke_id}")

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        chat_type = update.message.chat.type
        print(f"[LOG] /stop executed | Chat ID: {chat_id} | Type: {chat_type}")

        if chat_type in ['group', 'supergroup']:
            # Check if the user is an admin in group chats
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_ids = [admin.user.id for admin in admins]
            if update.message.from_user.id not in admin_ids:
                await update.message.reply_text("Only admins can stop the bot in this group.")
                return

            # Remove the chat from active_chats
            self.jokes_db.remove_active_chat(chat_id)
            await update.message.reply_text("Stopping random jokes in this group.")
        else:
            # Private chat: Remove the chat from active_chats
            self.jokes_db.remove_active_chat(chat_id)
            await update.message.reply_text("Stopping random jokes in your private chat.")

    async def joke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        active_chats = self.jokes_db.get_active_chats()
        chat_info = active_chats.get(chat_id, {'language': 'en', 'schedule': None})
        language = chat_info['language']
        joke, joke_id = self.jokes_db.get_random_joke_with_id(language)
        print(f"[LOG] /joke executed | Chat ID: {chat_id} | Language: {language} | Joke ID: {joke_id}")
        await update.message.reply_text(joke)

    async def add_joke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        print(f"[LOG] /addjoke executed | Chat ID: {chat_id}")
        args = context.args

        if len(args) < 2:
            await update.message.reply_text(
                "Usage: /addjoke <language> <joke>\n"
                "Example: /addjoke ar لماذا لا يلعب الهيكل العظمي مع الأصدقاء؟ لأنه ليس لديه أصدقاء."
            )
            return

        language = args[0].lower()
        joke = " ".join(args[1:])
        """
        if language not in self.SUPPORTED_LANGUAGES:
            await update.message.reply_text(
                f"Unsupported language. Supported languages: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )
            return
        """

        try:
            joke_id = self.jokes_db.add_joke(joke, language)
            print(f"[LOG] Joke added | Chat ID: {chat_id} | Language: {language} | Joke ID: {joke_id}")
            await update.message.reply_text(f"Joke added successfully in language: {language}")
        except Exception as e:
            print(f"[ERROR] Failed to add joke | Chat ID: {chat_id} | Error: {e}")
            await update.message.reply_text(f"Failed to add joke: {e}")

    async def set_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        chat_type = update.message.chat.type
        print(f"[LOG] /setlang executed | Chat ID: {chat_id}")

        #update available languages from database
        self.SUPPORTED_LANGUAGES = self.jokes_db.get_supported_languages()

        if chat_type in ['group', 'supergroup']:
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_ids = [admin.user.id for admin in admins]
            if update.message.from_user.id not in admin_ids:
                await update.message.reply_text("Only admins can set the language in this group.")
                return

        args = context.args
        if not args:
            await update.message.reply_text("Usage: /setlang <language> (e.g., /setlang fr, /setlang all)")
            return

        language = args[0].lower()
        if language not in self.SUPPORTED_LANGUAGES:
            await update.message.reply_text(
                f"Unsupported language. Supported languages: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )
            return

        self.jokes_db.set_preferred_language(chat_id, language)
        print(f"[LOG] Language set | Chat ID: {chat_id} | Language: {language}")
        if language == 'all':
            await update.message.reply_text("Preferred language set to: All languages.")
        else:
            await update.message.reply_text(f"Preferred language set to: {language}")

    async def set_schedule(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        chat_type = update.message.chat.type

        # Log the command execution
        print(f"[LOG] /setschedule executed | Chat ID: {chat_id}")

        # Allow admins to set schedule in groups; anyone can set it in private chats
        if chat_type in ['group', 'supergroup']:
            # Check if the user is an admin in group chats
            admins = await context.bot.get_chat_administrators(chat_id)
            admin_ids = [admin.user.id for admin in admins]
            if update.message.from_user.id not in admin_ids:
                await update.message.reply_text("Only admins can set the schedule in this group.")
                return

        # Extract the schedule from the command arguments
        args = context.args
        if not args:
            await update.message.reply_text(
                "Usage: /setschedule <minutes> (e.g., /setschedule 15)\n"
                "Default: 15 minutes\n"
                "Minimum: 1 minute"
            )
            return

        try:
            # Parse the input as minutes
            schedule_minutes = int(args[0])

            # Validate the schedule
            if schedule_minutes < 1:
                await update.message.reply_text("Schedule must be at least 1 minute.")
                return

        except ValueError:
            await update.message.reply_text("Invalid schedule. Please provide a number in minutes.")
            return

        # Convert minutes to seconds for scheduling
        schedule_seconds = schedule_minutes * 60

        # Set the schedule in the database
        self.jokes_db.set_schedule(chat_id, schedule_seconds)

        # Log and confirm the schedule change
        print(f"[LOG] Schedule set | Chat ID: {chat_id} | Schedule: {schedule_minutes} minutes ({schedule_seconds} seconds)")
        await update.message.reply_text(f"Joke-sending schedule set to: {schedule_minutes} minutes.")


    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        print(f"[LOG] /help executed | Chat ID: {chat_id}")
        help_text = (
            "Welcome to the Joke Bot!\n"
            "Available commands:\n"
            "/start - Start the bot\n"
            "/stop - Stop the bot\n"
            "/joke - Get a random joke\n"
            "/setlang <language> - Set the preferred language for jokes (e.g., /setlang fr, /setlang all)\n"
            "/setschedule <seconds> - Set the joke-sending interval in minutes (e.g., /setschedule 15)\n"
            "/addjoke <language> <joke> - Add a new joke to the database (e.g., /addjoke ar لماذا لا يلعب الهيكل العظمي مع الأصدقاء؟ لأنه ليس لديه أصدقاء.)\n"
            "/help - Show this help message"
        )
        await update.message.reply_text(help_text)

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        # Log the command execution
        print(f"[LOG] /stats executed | Chat ID: {chat_id}")

        # Fetch statistics from the database
        total_jokes = self.jokes_db.get_total_jokes()
        joke_count_per_language = self.jokes_db.get_joke_count_per_language()
        most_frequent_language = self.jokes_db.get_most_frequent_language() or ("N/A", 0)
        total_active_chats = self.jokes_db.get_total_active_chats()
        preferred_language_distribution = self.jokes_db.get_preferred_language_distribution()
        average_schedule = self.jokes_db.get_average_schedule()

        # Handle potential None values for longest and shortest jokes
        longest_joke = self.jokes_db.get_longest_joke() or (None, "N/A", 0)
        shortest_joke = self.jokes_db.get_shortest_joke() or (None, "N/A", float('inf'))

        # Format the response
        stats_text = (
            "📊 Database Statistics:\n"
            f"• Total Jokes: {total_jokes}\n"
            f"• Jokes Per Language: {joke_count_per_language}\n"
            f"• Most Frequent Language: {most_frequent_language[0]} ({most_frequent_language[1]} jokes)\n"
            f"• Total Active Chats: {total_active_chats}\n"
            f"• Preferred Language Distribution: {preferred_language_distribution}\n"
            f"• Average Schedule Interval: {average_schedule:.2f} seconds\n"
            f"• Longest Joke: \"{longest_joke[1]}\" (Length: {longest_joke[2]})\n"
            f"• Shortest Joke: \"{shortest_joke[1]}\" (Length: {shortest_joke[2]})"
        )
        await update.message.reply_text(stats_text)



    async def send_jokes_to_active_chats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Sends jokes to all active group chats and one joke to each active private chat.
        Usage: /sendjokes
        """
        chat_id = update.message.chat_id
        print(f"[LOG] /sendjokes executed | Chat ID: {chat_id}")

        # Fetch all active chats
        active_chats = self.jokes_db.get_active_chats()

        # Send jokes to group chats
        for chat_id, chat_info in active_chats.items():
            chat_type = update.message.chat.type
            if chat_type in ['group', 'supergroup']:
                language = chat_info['language']
                joke, joke_id = self.jokes_db.get_random_joke_with_id(language)
                try:
                    await context.bot.send_message(chat_id, joke)
                    print(f"[LOG] Joke sent to group chat | Chat ID: {chat_id} | Language: {language} | Joke ID: {joke_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send joke to group chat | Chat ID: {chat_id} | Error: {e}")

        # Send one joke to private chats
        for chat_id, chat_info in active_chats.items():
            chat_type = update.message.chat.type
            if chat_type == 'private':
                language = chat_info['language']
                joke, joke_id = self.jokes_db.get_random_joke_with_id(language)
                try:
                    await context.bot.send_message(chat_id, joke)
                    print(f"[LOG] Joke sent to private chat | Chat ID: {chat_id} | Language: {language} | Joke ID: {joke_id}")
                except Exception as e:
                    print(f"[ERROR] Failed to send joke to private chat | Chat ID: {chat_id} | Error: {e}")

        await update.message.reply_text("Jokes have been sent to all active chats!")

    def schedule_random_jokes(self, job_queue, chat_id):
        active_chats = self.jokes_db.get_active_chats()
        chat_info = active_chats.get(chat_id, {'language': 'en', 'schedule': 300})
        schedule = chat_info['schedule']

        if schedule is not None:
            job_queue.run_repeating(self.send_random_joke, interval=schedule, data=chat_id)
            print(f"[LOG] Scheduled jokes | Chat ID: {chat_id} | Interval: {schedule} seconds")

    async def send_random_joke(self, context: ContextTypes.DEFAULT_TYPE):
        chat_id = context.job.data
        active_chats = self.jokes_db.get_active_chats()
        chat_info = active_chats.get(chat_id, {'language': 'en', 'schedule': 300})
        language = chat_info['language']
        joke, joke_id = self.jokes_db.get_random_joke_with_id(language)

        try:
            await context.bot.send_message(chat_id, joke)
            print(f"[LOG] Random joke sent | Chat ID: {chat_id} | Language: {language} | Joke ID: {joke_id}")
        except Exception as e:
            print(f"[ERROR] Failed to send joke | Chat ID: {chat_id} | Error: {e}")