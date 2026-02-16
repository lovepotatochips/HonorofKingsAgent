import sqlite3
import json

db_path = "honor_of_kings.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT id, match_id, overall_rating FROM analyses LIMIT 5')
rows = cursor.fetchall()

print('数据库中的分析数据:')
for row in rows:
    print(f"ID: {row[0]}, Match ID: {row[1]}, Rating: {row[2]}")

cursor.execute('SELECT id, highlights FROM analyses WHERE id = ?', ('50ec69a8-8e6f-4fe0-970c-9a41b7a97966',))
row = cursor.fetchone()

if row:
    print(f"\n分析ID {row[0]} 的highlights:")
    print(json.dumps(json.loads(row[1]), indent=2, ensure_ascii=False))

conn.close()
