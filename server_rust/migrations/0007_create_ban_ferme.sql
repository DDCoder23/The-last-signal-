CREATE TABLE IF NOT EXISTS bansferme (

    client_id INTERGER,

    user_id UUID,

    auteur TEXT,

    raison TEXT,

    date_ban TIMESTAMP NOT NULL DEFAULT NOW(),

    date_déban TIMESTAMP NOT NULL

    

    

);
