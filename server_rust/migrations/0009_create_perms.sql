CREATE TABLE IF NOT EXISTS perms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    perm TEXT NOT NULL
);

INSERT INTO perms (name, perm)
VALUES
    ('Cyril', 'admin'),
    ('Morgan', 'Super admin');
