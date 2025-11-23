CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_cron;

/* DEFINICOES */

CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(50) PRIMARY KEY,
    pass TEXT
);

CREATE TABLE IF NOT EXISTS browser_sessions(
    session_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(50) NOT NULL REFERENCES users(username)
    ON DELETE CASCADE ON UPDATE CASCADE,
    token TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT
);

CREATE INDEX idx_sessions_username ON browser_sessions(username);
CREATE INDEX idx_sessions_expires_at ON browser_sessions(expires_at);


/* CREATE TABLE IF NOT EXISTS posts(
    postID SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    body VARCHAR(1000),
    creator INT NOT NULL REFERENCES users(userID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS responses(
    responseID SERIAL PRIMARY KEY,
    body VARCHAR(1000) NOT NULL,
    postID INT NOT NULL REFERENCES posts(postID)
    ON DELETE CASCADE ON UPDATE CASCADE,
    creatorID INT NOT NULL REFERENCES users(userID)
    ON DELETE CASCADE ON UPDATE CASCADE
); */

/* FUNÇÕES */

/* Checa hash de senha para um usuário no banco contra a fornecida */
CREATE OR REPLACE FUNCTION check_password(user_name VARCHAR(50), pword TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    stored_pass TEXT;
BEGIN
    SELECT pass INTO stored_pass FROM users WHERE username = user_name;

    IF stored_pass IS NULL THEN
        RETURN FALSE;
    END IF;

    RETURN stored_pass = crypt(pword, stored_pass);
END;
$$ LANGUAGE plpgsql;

/* TRIGGERS */

/* Troca senha em plaintext por senha com hash SHA256 */
CREATE OR REPLACE FUNCTION password_insert() RETURNS TRIGGER AS $$
BEGIN
    NEW.pass := crypt(NEW.pass, gen_salt('sha256crypt', 50000));

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER password_insert
BEFORE INSERT ON users
FOR EACH ROW EXECUTE FUNCTION password_insert();


/* CRON */

/* Limpa sessões a cada 10 minutos */
SELECT cron.schedule('cleanup_expired_sessions', '*/10 * * * *', 
    'DELETE FROM browser_sessions WHERE expires_at < CURRENT_TIMESTAMP'
);
