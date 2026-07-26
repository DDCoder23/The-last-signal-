CREATE TABLE IF NOT EXISTS accounts (

    account_id BIGSERIAL PRIMARY KEY,

    user_id UUID NOT NULL,

    username TEXT NOT NULL UNIQUE,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);
