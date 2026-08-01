CREATE TABLE perms (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
    perm TEXT NOT NULL
);

INSERT INTO perms (name,perm)
VALUES
    ('Cyril''admin'),
    ('Morgan','Super admin');
