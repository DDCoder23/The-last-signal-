CREATE TABLE IF NOT EXISTS sessions (

    session_id UUID PRIMARY KEY,

    account_id BIGINT,

    started_at TIMESTAMP NOT NULL DEFAULT NOW(),

    ended_at TIMESTAMP,

    disconnect_reason TEXT,

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE SET NULL

);
