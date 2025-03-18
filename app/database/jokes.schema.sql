-- jokes.test.sql

-- Create the jokes table with a language column
CREATE TABLE IF NOT EXISTS jokes (
    id INTEGER PRIMARY KEY,
    joke TEXT NOT NULL,
    language TEXT NOT NULL  -- Add a column for the joke's language
);

-- Create the active_chats table with preferred_language and schedule columns
CREATE TABLE IF NOT EXISTS active_chats (
    chat_id INTEGER PRIMARY KEY,
    preferred_language TEXT NOT NULL DEFAULT 'en',  -- Default language is English
    schedule INTEGER NOT NULL DEFAULT 300          -- Default schedule is 5 minutes (300 seconds)
);