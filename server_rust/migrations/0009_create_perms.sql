CREATE TABLE IF NOT EXISTS perms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_name TEXT NOT NULL,
    perm TEXT NOT NULL,
    UNIQUE (account_name, perm)
    FOREIGN KEY (account_name)
        REFERENCES accounts(account)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT OR IGNORE INTO perms (account_name, perm)
VALUES
    ('Cyril', 'dev'),
    ('Morgan', 'Super dev');
