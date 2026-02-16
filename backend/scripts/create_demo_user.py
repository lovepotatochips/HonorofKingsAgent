import sqlite3
import json

db_path = "honor_of_kings.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

user_id = "user_1771059406553_demo"

cursor.execute('''
    INSERT OR REPLACE INTO users (id, nickname, avatar, rank, stars, favorite_heroes, preferences)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    user_id,
    "演示用户",
    "https://picsum.photos/100/100",
    "黄金",
    3,
    json.dumps([]),
    json.dumps({})
))

conn.commit()

print(f"已创建用户: {user_id}")

conn.close()
