import sqlite3

db_path = "honor_of_kings.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT id, nickname FROM users')
rows = cursor.fetchall()

print('数据库中的用户数据:')
for row in rows:
    print(row)

conn.close()
