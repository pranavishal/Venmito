import sqlite3

# Connect to the database
connection = sqlite3.connect("venmito.db")
cursor = connection.cursor()

# Define and run your queries
queries = [
    "SELECT * FROM People LIMIT 5;",
    "SELECT p.firstName, p.surname, pr.promotion, pr.responded FROM Promotions pr JOIN People p ON pr.client_email = p.email LIMIT 10;",
    "SELECT s.firstName AS sender, r.firstName AS recipient, t.amount FROM Transfers t JOIN People s ON t.sender_id = s.id JOIN People r ON t.recipient_id = r.id LIMIT 10;",
    """
    SELECT 
        t.customer_id,
        p.firstName,
        p.surname,
        SUM(t.total_price) AS total_spending
    FROM 
        Transactions t
    JOIN 
        People p
    ON 
        t.customer_id = p.id
    GROUP BY 
        t.customer_id, p.firstName, p.surname
    ORDER BY 
        total_spending DESC
    LIMIT 10;
    """
]

for query in queries:
    print(f"Running query: {query}")
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("\n")

# Close the connection
connection.close()
