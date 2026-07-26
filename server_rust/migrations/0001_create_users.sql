CREATE TABLE users (

    user_id UUID PRIMARY KEY,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()

);
