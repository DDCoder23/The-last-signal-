CREATE TABLE IF NOT EXISTS bansferme (


    user_id UUID PRIMARY KEY,

    auteur TEXT,

    raison TEXT,

    date_ban TIMESTAMP NOT NULL DEFAULT NOW(),

    date_deban TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)

    

    

);
