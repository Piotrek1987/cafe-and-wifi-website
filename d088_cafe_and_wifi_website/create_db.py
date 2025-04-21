import sqlite3

conn = sqlite3.connect("cafes.db")  # Make sure the path is correct
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(cafe);")
columns = cursor.fetchall()

for column in columns:
    print(column)
