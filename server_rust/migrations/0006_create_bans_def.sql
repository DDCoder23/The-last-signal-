CREATE TABLE IF NOT EXISTS bansdef (

    client_id BIGSERIAL PRIMARY KEY,

    user_id UUID,

    auteur TEXT,

    raison TEXT,

    date_ban TIMESTAMP NOT NULL DEFAULT NOW(),

    

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL

);
