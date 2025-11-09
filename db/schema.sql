CREATE EXTENSION IF NOT EXISTS pgcrypto;

/* DEFINICOES */

CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(50) PRIMARY KEY,
    pass TEXT
);

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

CREATE OR REPLACE FUNCTION password_insert() RETURNS TRIGGER AS $$
BEGIN
    NEW.pass := crypt(NEW.pass, gen_salt('sha256crypt', 50000));

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER password_insert
BEFORE INSERT ON users
FOR EACH ROW EXECUTE FUNCTION password_insert();
