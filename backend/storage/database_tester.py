import sqlite3

# Connect to the database
connection = sqlite3.connect("venmito.db")
cursor = connection.cursor()

# Define and run your queries
queries = [
    """
SELECT 
    People.country AS country,
    SUM(Transactions.total_price) AS total_spent
FROM 
    Transactions
JOIN 
    People
ON 
    Transactions.customer_id = People.id
GROUP BY 
    People.country
ORDER BY 
    total_spent DESC;


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
