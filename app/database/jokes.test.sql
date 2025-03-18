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

-- Insert sample jokes in different languages
INSERT INTO jokes (joke, language) VALUES ('Why don’t skeletons fight each other? They don’t have the guts.', 'en');
INSERT INTO jokes (joke, language) VALUES ('Pourquoi les squelettes ne se battent-ils pas ? Ils n’ont pas de courage.', 'fr');
INSERT INTO jokes (joke, language) VALUES ('¿Por qué los esqueletos no pelean entre ellos? No tienen el coraje.', 'es');
INSERT INTO jokes (joke, language) VALUES ('لماذا لا يلعب الهيكل العظمي مع الأصدقاء؟ لأنه ليس لديه أصدقاء.', 'ar');

-- jokes.test.sql

-- Create the jokes table with a language column
CREATE TABLE IF NOT EXISTS jokes (
    id INTEGER PRIMARY KEY,
    joke TEXT NOT NULL,
    language TEXT NOT NULL  -- Add a column for the joke's language
);

-- Create the active_chats table with a preferred_language column
CREATE TABLE IF NOT EXISTS active_chats (
    chat_id INTEGER PRIMARY_KEY,
    preferred_language TEXT NOT_NULL DEFAULT 'en'  -- Default language is English
);

-- Arabic Jokes
INSERT INTO jokes (joke, language) VALUES ('لماذا السمك لا يتكلم؟ لأنه يخشى أن يُفهم!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('ما هو أطول شيء في العالم؟ حبل الكذب!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('كيف تعرف أن الجمل مريض؟ عندما يقول: أنا بعير!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('ما هو الشيء الذي يدور ولا يتحرك؟ الساعة!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('لماذا الطيور تطير؟ لأنها لا تستطيع المشي على الماء!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('ما هو الشيء الذي كلما زاد نقص؟ العمر!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('من هو الشخص الذي يرى عدوه وصديقه بعين واحدة؟ الأعمى!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('ما هو الشيء الذي له أربع أرجل ولا يستطيع المشي؟ الكرسي!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('لماذا الفيل أكبر من البعوضة؟ لأنه لو كان العكس لكان كارثة!', 'Arabic');
INSERT INTO jokes (joke, language) VALUES ('ما هو الشيء الذي يمشي بلا قدمين؟ السحاب!', 'Arabic');
-- ... Continue with more Arabic jokes (up to 100 total).

-- English Jokes
INSERT INTO jokes (joke, language) VALUES ('Why don’t skeletons fight each other? They don’t have the guts!', 'English');
INSERT INTO jokes (joke, language) VALUES ('What do you call fake spaghetti? An impasta!', 'English');
INSERT INTO jokes (joke, language) VALUES ('Why did the scarecrow win an award? Because he was outstanding in his field!', 'English');
INSERT INTO jokes (joke, language) VALUES ('What has keys but can’t open locks? A keyboard!', 'English');
INSERT INTO jokes (joke, language) VALUES ('Why don’t eggs tell jokes? They’d crack each other up!', 'English');
INSERT INTO jokes (joke, language) VALUES ('What do you call cheese that isn’t yours? Nacho cheese!', 'English');
INSERT INTO jokes (joke, language) VALUES ('Why did the math book look so sad? It had too many problems!', 'English');
INSERT INTO jokes (joke, language) VALUES ('What do you call a bear with no teeth? A gummy bear!', 'English');
INSERT INTO jokes (joke, language) VALUES ('Why don’t scientists trust atoms? Because they make up everything!', 'English');
INSERT INTO jokes (joke, language) VALUES ('What do you call a fish wearing a bowtie? Sofishticated!', 'English');
-- ... Continue with more English jokes (up to 100 total).