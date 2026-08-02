CREATE TABLE IF NOT EXISTS banssursis (


    user_id UUID NOT NULL,

    auteur TEXT,

    raison TEXT,

    date_ban TIMESTAMP NOT NULL DEFAULT NOW(),
    sursis TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

    


    
