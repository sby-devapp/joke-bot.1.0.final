# Joke Bot (Version 1.0)

A Telegram bot that sends random jokes to users. Supports multiple languages and customizable joke-sending schedules.

## Features
- Random jokes in multiple languages.
- Customizable joke-sending intervals.
- Admin controls for group chats.
- Add new jokes via `/addjoke`.

## Setup
1. git clone https://github.com/your-username/joke-bot.git
2. cd joke-bot
3. Install dependencies: `pip install -r requirements.txt`.
4. Add your Telegram bot token to a `.env` file.
5. initialize database: `python app/init_databse.py`
5. Run the bot: `python app/main.py`.

## Commands: 
- `/start`: Start the bot.
- `/stop`: Stop the bot.
- `/joke`: Get a random joke.
- `/setlang <language>`: Set the preferred language for jokes.
- `/setschedule <seconds>`: Set the joke-sending interval.
- `/addjoke <language> <joke>`: Add a new joke to the database.
- `/stats`: View database statistics.
- `/help`: Show help message.
     

## License
MIT License

