CREATE TABLE IF NOT EXISTS bansperm (
    user_id TEXT NOT NULL PRIMARY KEY,
    auteur TEXT NOT NULL,
    raison TEXT NOT NULL,
    date_ban TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);
