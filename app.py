import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyNewPassword123!",
    database="edupro_db"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM students")

rows = cursor.fetchall()

print("Student Records:")
for row in rows:
    print(row)

cursor.close()
conn.close()