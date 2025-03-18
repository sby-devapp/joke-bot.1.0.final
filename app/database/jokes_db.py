import os
import sqlite3


class JokesDB:
    def __init__(self, db_path):
        """
        Initializes the JokesDB instance with the path to the SQLite database.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        :return: A connection object.
        """
        return sqlite3.connect(self.db_path)

    def init_from_sql_file(self, sql_file_path):
        """
        Initializes the database schema from an SQL file.
        :param sql_file_path: Path to the SQL file containing the schema.
        """
        if not os.path.exists(sql_file_path):
            raise FileNotFoundError(f"SQL file not found at: {sql_file_path}")

        with open(sql_file_path, 'r') as f:
            sql_script = f.read()

        with self.connect() as conn:
            conn.executescript(sql_script)
            conn.commit()

    def add_joke(self, joke, language):
        """
        Adds a new joke to the database.
        :param joke: The joke text.
        :param language: The language of the joke.
        :return: The ID of the newly added joke.
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO jokes (joke, language) VALUES (?, ?)",
                (joke, language)
            )
            conn.commit()
            return cursor.lastrowid

    def get_random_joke_with_id(self, language='en'):
        """
        Fetches a random joke from the database for the specified language and returns the joke along with its ID.
        If language is 'all', fetches a random joke from any language.
        :param language: The language of the joke to fetch.
        :return: A tuple containing the joke and its ID.
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            if language == 'all':
                cursor.execute(
                    "SELECT id, joke FROM jokes ORDER BY RANDOM() LIMIT 1"
                )
            else:
                cursor.execute(
                    "SELECT id, joke FROM jokes WHERE language = ? ORDER BY RANDOM() LIMIT 1",
                    (language,)
                )
            result = cursor.fetchone()
            if result:
                joke_id, joke = result
                return joke, joke_id
            else:
                return "No jokes available in this language.", None

    def get_supported_languages(self):
        """
        Retrieves all unique languages from the jokes table.
        :return: A list of supported languages.
        """
        with self.connect() as conn:
            cursor = conn.execute("SELECT DISTINCT language FROM jokes")
            languages = [row[0] for row in cursor.fetchall()]
        return languages + ['all']  # Include 'all' as an option

    def add_active_chat(self, chat_id, preferred_language='en', schedule=900):
        """
        Adds a chat ID to the active_chats table with a preferred language and schedule.
        :param chat_id: The ID of the chat to add.
        :param preferred_language: The preferred language for jokes (default is 'en').
        :param schedule: The schedule interval in seconds (default is 300 seconds).
        """
        with self.connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO active_chats (chat_id, preferred_language, schedule) VALUES (?, ?, ?)",
                (chat_id, preferred_language, schedule)
            )
            conn.commit()

    def remove_active_chat(self, chat_id):
        """
        Removes a chat ID from the active_chats table.
        :param chat_id: The ID of the chat to remove.
        """
        with self.connect() as conn:
            conn.execute("DELETE FROM active_chats WHERE chat_id = ?", (chat_id,))
            conn.commit()

    def get_active_chats(self):
        """
        Retrieves all active chat IDs, their preferred languages, and schedules.
        :return: A dictionary of chat IDs with their language and schedule.
        """
        with self.connect() as conn:
            cursor = conn.execute("SELECT chat_id, preferred_language, schedule FROM active_chats")
            return {row[0]: {'language': row[1], 'schedule': row[2]} for row in cursor.fetchall()}

    def set_preferred_language(self, chat_id, language):
        """
        Sets the preferred language for a chat.
        :param chat_id: The ID of the chat.
        :param language: The preferred language for jokes.
        """
        with self.connect() as conn:
            conn.execute(
                "UPDATE active_chats SET preferred_language = ? WHERE chat_id = ?",
                (language, chat_id)
            )
            conn.commit()

    def set_schedule(self, chat_id, scheduleb):
        """
        Sets the schedule interval for a chat.
        :param chat_id: The ID of the chat.
        :param schedule: The schedule interval in seconds.
        """
        with self.connect() as conn:
            conn.execute(
                "UPDATE active_chats SET schedule = ? WHERE chat_id = ?",
                (schedule, chat_id)
            )
            conn.commit()

    def get_total_jokes(self):
        """
        Retrieves the total number of jokes in the database.
        :return: Total number of jokes.
        """
        with self.connect() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM jokes")
            return cursor.fetchone()[0]

    def get_joke_count_per_language(self):
        """
        Retrieves the count of jokes per language.
        :return: A dictionary of language counts.
        """
        with self.connect() as conn:
            cursor = conn.execute("SELECT language, COUNT(*) FROM jokes GROUP BY language")
            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_most_frequent_language(self):
        """
        Retrieves the most frequent language in the jokes table.
        :return: A tuple containing the language and its count.
        """
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT language, COUNT(*) AS count FROM jokes GROUP BY language ORDER BY count DESC LIMIT 1"
            )
            return cursor.fetchone()

    def get_total_active_chats(self):
        """
        Retrieves the total number of active chats.
        :return: Total number of active chats.
        """
        with self.connect() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM active_chats")
            return cursor.fetchone()[0]

    def get_preferred_language_distribution(self):
        """
        Retrieves the distribution of preferred languages across active chats.
        :return: A dictionary of language distributions.
        """
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT preferred_language, COUNT(*) FROM active_chats GROUP BY preferred_language"
            )
            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_average_schedule(self):
        """
        Retrieves the average schedule interval across active chats.
        :return: Average schedule interval in seconds.
        """
        with self.connect() as conn:
            cursor = conn.execute("SELECT AVG(schedule) FROM active_chats")
            return cursor.fetchone()[0] or 0

    def get_longest_joke(self):
        """
        Retrieves the longest joke in the database.
        :return: A tuple containing the joke and its length.
        """
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT joke, LENGTH(joke) AS length FROM jokes ORDER BY length DESC LIMIT 1"
            )
            return cursor.fetchone()

    def get_shortest_joke(self):
        """
        Retrieves the shortest joke in the database.
        :return: A tuple containing the joke and its length.
        """
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT joke, LENGTH(joke) AS length FROM jokes ORDER BY length ASC LIMIT 1"
            )
            return cursor.fetchone()
    
    def get_longest_joke(self):
        """
        Retrieves the longest joke in the database.
        :return: A tuple containing the joke ID, joke text, and its length.
        """
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT id, joke, LENGTH(joke) AS length FROM jokes ORDER BY length DESC LIMIT 1"
            )
            result = cursor.fetchone()
            if result:
                return result
            else:
                return (None, "No jokes available.", 0)

    def get_shortest_joke(self):
        """
        Retrieves the shortest joke in the database.
        :return: A tuple containing the joke ID, joke text, and its length.
        """
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT id, joke, LENGTH(joke) AS length FROM jokes ORDER BY length ASC LIMIT 1"
            )
            result = cursor.fetchone()
            if result:
                return result
            else:
                return (None, "No jokes available.", float('inf'))