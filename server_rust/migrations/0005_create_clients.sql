CREATE TABLE IF NOT EXISTS clients (

    client_id BIGSERIAL,

    user_id UUID PRIMARY KEY,

    platform TEXT,

    game_version TEXT,

    os TEXT,

    cpu TEXT,

    gpu TEXT,

    first_seen TIMESTAMP NOT NULL DEFAULT NOW(),

    last_seen TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL

);
