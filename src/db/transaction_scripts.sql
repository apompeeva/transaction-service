CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type VARCHAR(255) NOT NULL CHECK (type IN ('deposit', 'withdrawal')),
    amount INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


INSERT INTO transactions (user_id, type, amount, created_at)
VALUES (1, 'deposit', 50, CURRENT_TIMESTAMP);

SELECT * FROM transactions;

UPDATE transactions
SET type = 'withdrawal', amount = 30, created_at = CURRENT_TIMESTAMP
WHERE id = 1;

DELETE FROM transactions WHERE id = 1;

DROP TABLE transactions;
