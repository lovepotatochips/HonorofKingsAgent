import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import json
from datetime import datetime, timedelta

SAMPLE_MATCHES = [
    {
        "hero_name": "鲁班七号",
        "position": "archer",
        "result": "胜利",
        "duration": 1230,
        "kills": 12,
        "deaths": 3,
        "assists": 8,
        "gold": 18500,
        "damage": 185000,
        "damage_taken": 35000,
        "healing": 0,
        "kda": 6.7,
        "participation_rate": 0.75,
        "equipment_list": [
            {"name": "急速战靴", "price": 710},
            {"name": "末世", "price": 2160},
            {"name": "无尽战刃", "price": 2140},
            {"name": "破晓", "price": 3400},
            {"name": "泣血之刃", "price": 1740},
            {"name": "破军", "price": 2950}
        ],
        "inscription": {"name": "10祸源 10鹰眼 10狩猎"}
    },
    {
        "hero_name": "亚瑟",
        "position": "warrior",
        "result": "失败",
        "duration": 1180,
        "kills": 5,
        "deaths": 7,
        "assists": 12,
        "gold": 15200,
        "damage": 98000,
        "damage_taken": 68000,
        "healing": 8500,
        "kda": 2.4,
        "participation_rate": 0.68,
        "equipment_list": [
            {"name": "抵抗之靴", "price": 710},
            {"name": "暗影战斧", "price": 2190},
            {"name": "冰痕之握", "price": 2100},
            {"name": "不死鸟之眼", "price": 2100},
            {"name": "霸者重装", "price": 2070},
            {"name": "贤者的庇护", "price": 2080}
        ],
        "inscription": {"name": "10异变 10鹰眼 10狩猎"}
    },
    {
        "hero_name": "妲己",
        "position": "mage",
        "result": "胜利",
        "duration": 1350,
        "kills": 8,
        "deaths": 4,
        "assists": 15,
        "gold": 16800,
        "damage": 142000,
        "damage_taken": 42000,
        "healing": 0,
        "kda": 5.8,
        "participation_rate": 0.82,
        "equipment_list": [
            {"name": "冷静之靴", "price": 710},
            {"name": "回响之杖", "price": 2100},
            {"name": "博学者之怒", "price": 2700},
            {"name": "虚无法杖", "price": 2750},
            {"name": "辉月", "price": 1990},
            {"name": "贤者之书", "price": 2950}
        ],
        "inscription": {"name": "10梦魇 10心眼 10狩猎"}
    },
    {
        "hero_name": "孙悟空",
        "position": "assassin",
        "result": "胜利",
        "duration": 1080,
        "kills": 15,
        "deaths": 5,
        "assists": 6,
        "gold": 19200,
        "damage": 165000,
        "damage_taken": 38000,
        "healing": 3200,
        "kda": 4.2,
        "participation_rate": 0.71,
        "equipment_list": [
            {"name": "追击刀锋", "price": 710},
            {"name": "暗影战斧", "price": 2190},
            {"name": "宗师之力", "price": 2100},
            {"name": "破军", "price": 2950},
            {"name": "泣血之刃", "price": 1740},
            {"name": "名刀", "price": 1800}
        ],
        "inscription": {"name": "10异变 10鹰眼 10隐匿"}
    },
    {
        "hero_name": "张飞",
        "position": "support",
        "result": "失败",
        "duration": 1420,
        "kills": 2,
        "deaths": 8,
        "assists": 18,
        "gold": 12800,
        "damage": 45000,
        "damage_taken": 89000,
        "healing": 32000,
        "kda": 2.5,
        "participation_rate": 0.78,
        "equipment_list": [
            {"name": "疾步之靴", "price": 710},
            {"name": "极影", "price": 1900},
            {"name": "近卫荣耀", "price": 1900},
            {"name": "救赎之翼", "price": 1800},
            {"name": "星泉", "price": 1750},
            {"name": "奔狼纹章", "price": 1800}
        ],
        "inscription": {"name": "10宿命 10虚空 10调和"}
    },
    {
        "hero_name": "后羿",
        "position": "archer",
        "result": "胜利",
        "duration": 1180,
        "kills": 10,
        "deaths": 4,
        "assists": 10,
        "gold": 17800,
        "damage": 178000,
        "damage_taken": 36000,
        "healing": 0,
        "kda": 5.0,
        "participation_rate": 0.73,
        "equipment_list": [
            {"name": "急速战靴", "price": 710},
            {"name": "末世", "price": 2160},
            {"name": "无尽战刃", "price": 2140},
            {"name": "破晓", "price": 3400},
            {"name": "泣血之刃", "price": 1740},
            {"name": "破军", "price": 2950}
        ],
        "inscription": {"name": "10祸源 10鹰眼 10狩猎"}
    },
    {
        "hero_name": "韩信",
        "position": "assassin",
        "result": "失败",
        "duration": 980,
        "kills": 6,
        "deaths": 8,
        "assists": 4,
        "gold": 13500,
        "damage": 95000,
        "damage_taken": 52000,
        "healing": 0,
        "kda": 1.3,
        "participation_rate": 0.52,
        "equipment_list": [
            {"name": "追击刀锋", "price": 710},
            {"name": "暗影战斧", "price": 2190},
            {"name": "宗师之力", "price": 2100},
            {"name": "破军", "price": 2950},
            {"name": "泣血之刃", "price": 1740},
            {"name": "名刀", "price": 1800}
        ],
        "inscription": {"name": "10异变 10鹰眼 10隐匿"}
    },
    {
        "hero_name": "貂蝉",
        "position": "mage",
        "result": "胜利",
        "duration": 1250,
        "kills": 9,
        "deaths": 5,
        "assists": 11,
        "gold": 16200,
        "damage": 138000,
        "damage_taken": 45000,
        "healing": 28000,
        "kda": 4.0,
        "participation_rate": 0.76,
        "equipment_list": [
            {"name": "冷静之靴", "price": 710},
            {"name": "回响之杖", "price": 2100},
            {"name": "博学者之怒", "price": 2700},
            {"name": "虚无法杖", "price": 2750},
            {"name": "辉月", "price": 1990},
            {"name": "贤者之书", "price": 2950}
        ],
        "inscription": {"name": "10梦魇 10心眼 10狩猎"}
    }
]


def import_sample_matches(user_id: str):
    print(f"开始为用户 {user_id} 导入示例对局数据...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "honor_of_kings.db")
    db_path = os.path.abspath(db_path)
    
    print(f"数据库路径: {db_path}")
    print(f"脚本目录: {script_dir}")
    
    if not os.path.exists(db_path):
        print(f"错误：数据库文件不存在于 {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    imported_count = 0
    base_time = datetime.utcnow()
    
    for i, match_data in enumerate(SAMPLE_MATCHES):
        match_id = f"match_{i}_{user_id[:8]}"
        created_at = (base_time - timedelta(hours=i*2)).isoformat()
        
        cursor.execute("""
            INSERT INTO matches (id, user_id, hero_name, position, result, duration, 
            kills, deaths, assists, gold, damage, damage_taken, healing, 
            kda, participation_rate, equipment_list, inscription, rank, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match_id,
            user_id,
            match_data["hero_name"],
            match_data["position"],
            match_data["result"],
            match_data["duration"],
            match_data["kills"],
            match_data["deaths"],
            match_data["assists"],
            match_data["gold"],
            match_data["damage"],
            match_data["damage_taken"],
            match_data["healing"],
            match_data["kda"],
            match_data["participation_rate"],
            json.dumps(match_data["equipment_list"]),
            json.dumps(match_data["inscription"]),
            "黄金",
            created_at
        ))
        
        imported_count += 1
        print(f"✓ 导入对局: {match_data['hero_name']} - {match_data['result']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n导入完成！共导入 {imported_count} 条对局记录")


if __name__ == "__main__":
    try:
        user_id = "user_1771059406553_demo"
        import_sample_matches(user_id)
        print(f"\n用户ID: {user_id}")
        print("请在浏览器中刷新页面查看对局数据")
    except Exception as e:
        print(f"导入失败：{e}")
        import traceback
        traceback.print_exc()
