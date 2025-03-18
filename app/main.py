import os
from telegram.ext import Application, CommandHandler
from bot import JokeBot
from database.jokes_db import JokesDB


class App:
    def __init__(self):
        # Resolve the root directory of the project
        self.root = os.path.dirname(os.path.abspath(__file__))
        print(f"Project root: {self.root}")

    def get_file(self, relative_path):
        """
        Resolves and returns the absolute path to a file.
        :param relative_path: Relative path to the file
        :return: Absolute path to the file
        """
        absolute_path = os.path.normpath(os.path.join(self.root, relative_path))
        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"File not found at: {absolute_path}")
        return absolute_path

    def main(self):
        try:
            # Load the bot token using UTF-8 encoding
            token_path = self.get_file('token.txt')
            with open(token_path, 'r', encoding='utf-8') as f:
                TOKEN = f.read().strip()

            # Initialize the database connection
            db = JokesDB(self.get_file('database/jokes.db'))

            # Create the bot instance
            bot = JokeBot(db)

            # Create the Application with JobQueue enabled
            application = Application.builder().token(TOKEN).build()

            # Register command handlers
            application.add_handler(CommandHandler("start", bot.start))
            application.add_handler(CommandHandler("stop", bot.stop))
            application.add_handler(CommandHandler("joke", bot.joke))
            application.add_handler(CommandHandler("setlang", bot.set_language))
            application.add_handler(CommandHandler("setschedule", bot.set_schedule))
            application.add_handler(CommandHandler("addjoke", bot.add_joke))
            application.add_handler(CommandHandler("stats", bot.stats))
            application.add_handler(CommandHandler("help", bot.help))
            application.add_handler(CommandHandler("sendjokes", bot.send_jokes_to_active_chats))

            # Restore active chats and schedule jobs
            #self.restore_active_chats(application, bot)

            # Start the bot
            print("Bot is running...")
            application.run_polling()

        except Exception as e:
            print(f"Error: {e}")

    def restore_active_chats(self, application, bot):
        """
        Restores active chats and schedules joke-sending jobs for each chat.
        """
        print("[LOG] Restoring active chats...")
        active_chats = bot.jokes_db.get_active_chats()
        for chat_id, chat_info in active_chats.items():
            language = chat_info['language']
            schedule = chat_info['schedule']
            print(f"[LOG] Restored chat | Chat ID: {chat_id} | Language: {language} | Schedule: {schedule}")

            # Only schedule jokes for group chats with a valid schedule
            if schedule is not None:
                bot.schedule_random_jokes(application.job_queue, chat_id)


if __name__ == "__main__":
    app = App()
    app.main()