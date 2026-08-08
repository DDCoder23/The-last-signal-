CREATE TABLE IF NOT EXISTS perms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    perm TEXT NOT NULL,
    UNIQUE (name, perm)
);

INSERT OR IGNORE INTO perms (name, perm)
VALUES
    ('Cyril', 'admin'),
    ('Morgan', 'Super admin');
