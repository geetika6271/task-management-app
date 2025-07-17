import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Query all records from the tasks table
cursor.execute('SELECT * FROM tasks')

# Fetch all rows
rows = cursor.fetchall()

# Print records
for row in rows:
    print(f'ID: {row[0]}, Task: {row[1]}, Done: {row[2]}')

# Close the connection
conn.close()
