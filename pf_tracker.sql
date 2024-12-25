CREATE TABLE IF NOT EXISTS finance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    amount FLOAT NOT NULL,
    category STRING NOT NULL,
    description TEXT
);