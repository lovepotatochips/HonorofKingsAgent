import sqlite3

db_path = "honor_of_kings.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT id, user_id, hero_name, result FROM matches LIMIT 5')
rows = cursor.fetchall()

print('数据库中的对局数据:')
for row in rows:
    print(row)

conn.close()
