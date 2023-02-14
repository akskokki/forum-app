DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS topics CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS messages CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    description TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    time TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER REFERENCES threads,
    user_id INTEGER REFERENCES users,
    time TIMESTAMP
);