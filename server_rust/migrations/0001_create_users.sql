CREATE TABLE IF NOT EXISTS users (

    user_id UUID PRIMARY KEY,

    email TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    last_login TIMESTAMP

);
