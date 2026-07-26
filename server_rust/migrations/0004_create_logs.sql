CREATE TABLE IF NOT EXISTS logs (

    log_id BIGSERIAL PRIMARY KEY,

    session_id UUID NOT NULL,

    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),

    level VARCHAR(16) NOT NULL,

    module TEXT NOT NULL,

    message TEXT NOT NULL,

    FOREIGN KEY (session_id)
        REFERENCES sessions(session_id)
        ON DELETE CASCADE

);
