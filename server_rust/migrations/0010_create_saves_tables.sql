CREATE TABLE IF NOT EXISTS stuff (
    stuff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE CASCADE,

    UNIQUE (account_id, item_name)
);
CREATE TABLE IF NOT EXISTS echecs (
    echec_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    categorie TEXT NOT NULL,
    objet TEXT NOT NULL,
    nombre INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE CASCADE,

    UNIQUE (account_id, categorie, objet)
);
