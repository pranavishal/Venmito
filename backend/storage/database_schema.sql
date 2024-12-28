-- Create the People table
CREATE TABLE People (
    id INT PRIMARY KEY,
    email VARCHAR(255),
    phone VARCHAR(20), -- Changed from telephone to phone
    firstName VARCHAR(50),
    surname VARCHAR(50),
    city VARCHAR(50),
    country VARCHAR(50),
    Android BOOLEAN,
    iPhone BOOLEAN,
    Desktop BOOLEAN
);


-- Create the Promotions table
-- Updated Promotions table
CREATE TABLE Promotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Changed from promotion_id to id
    client_email VARCHAR(255),
    phone VARCHAR(20), 
    promotion VARCHAR(50),
    responded VARCHAR(10),
    FOREIGN KEY (client_email) REFERENCES People(email)
);


-- Create the Transactions table
CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Add a unique identifier for every row
    transaction_id INTEGER NOT NULL,
    customer_id INT,
    phone VARCHAR(20),
    store VARCHAR(100),
    item_name VARCHAR(50),
    quantity INT,
    price_per_item FLOAT,
    total_price FLOAT,
    FOREIGN KEY (customer_id) REFERENCES People(id)
);


-- Create the Transfers table
CREATE TABLE Transfers (
    transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INT,
    recipient_id INT,
    amount FLOAT,
    date DATE,
    FOREIGN KEY (sender_id) REFERENCES People(id),
    FOREIGN KEY (recipient_id) REFERENCES People(id)
);
