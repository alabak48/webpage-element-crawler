import psycopg2

# Define the connection parameters
db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "admin1234"
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Create a cursor
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM page")

# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor and the connection
cursor.close()
conn.close()
