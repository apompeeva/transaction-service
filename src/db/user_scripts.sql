CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    balance INTEGER DEFAULT 0,
    verified BOOLEAN DEFAULT FALSE
);

INSERT INTO users (login, password, balance, verified)
VALUES ('user1', 'password1', 100, TRUE);

SELECT * FROM users;

UPDATE users
SET login = 'new_user1', password = 'new_password1', balance = 150, verified = FALSE
WHERE id = 1;

DELETE FROM users WHERE id = 1;

DROP TABLE users;
