CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    description TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    time TIMESTAMP
);

CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER REFERENCES threads,
    user_id INTEGER REFERENCES users,
    time TIMESTAMP
);