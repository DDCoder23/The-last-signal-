CREATE TABLE IF NOT EXISTS bansperm (

    client_id INTERGER,

    user_id UUID,

    auteur TEXT,

    raison TEXT,

    date_ban TIMESTAMP NOT NULL DEFAULT NOW(),

    

    

);
