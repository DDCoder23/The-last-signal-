CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    account_id INTEGER,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TEXT,
    disconnect_reason TEXT,

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE SET NULL
);
