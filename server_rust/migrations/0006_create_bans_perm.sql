CREATE TABLE IF NOT EXISTS bansperm (
    user_id UUID NOT NULL,
    auteur TEXT NOT NULL,
    raison TEXT NOT NULL,
    date_ban TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
