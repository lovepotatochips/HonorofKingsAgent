import sqlite3

def add_image_url_column():
    db_path = "backend/honor_of_kings.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(heroes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'image_url' not in columns:
            cursor.execute("ALTER TABLE heroes ADD COLUMN image_url VARCHAR(500)")
            conn.commit()
            print("✓ 成功添加 image_url 列到 heroes 表")
        else:
            print("✓ image_url 列已存在，跳过添加")
            
    except Exception as e:
        print(f"✗ 添加列失败：{e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_image_url_column()
