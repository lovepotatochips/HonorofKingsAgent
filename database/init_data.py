import json
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.hero import Hero, HeroEquipment, HeroInscription
from app.models.user import User


def init_sample_data():
    db = SessionLocal()
    
    try:
        if db.query(Hero).count() > 0:
            print("数据库已有数据，跳过初始化")
            return
        
        sample_heroes = [
            {
                "name": "鲁班七号",
                "title": "鲁班大师号机关造物",
                "position": "archer",
                "difficulty": "easy",
                "description": "鲁班七号是鲁班大师发明的高智能机关造物，拥有极高的射击天赋。",
                "skills": [
                    {"name": "火力压制", "description": "向指定方向扫射，造成物理伤害", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
                    {"name": "无敌鲨嘴炮", "description": "向指定方向发射炮弹，造成物理伤害并附带目标已损生命值的伤害", "cooldown": "12秒", "cost": "50法力", "type": "主动技能"},
                    {"name": "空中支援", "description": "召唤河豚飞艇对指定区域进行火力打击", "cooldown": "36秒", "cost": "100法力", "type": "大招"}
                ],
                "passive_skill": {"name": "火力压制", "description": "连续的普攻命中会积累火力层数，叠满后造成范围爆炸伤害"},
                "win_rate": 0.52,
                "ban_rate": 0.05,
                "pick_rate": 0.35,
                "counter_heroes": ["程咬金", "张飞", "庄周"],
                "countered_by_heroes": ["兰陵王", "阿轲", "韩信"],
                "version": "1.0.0"
            },
            {
                "name": "亚瑟",
                "title": "圣光之盾",
                "position": "warrior",
                "difficulty": "easy",
                "description": "亚瑟是王者峡谷中非常均衡的战士，适合新手玩家。",
                "skills": [
                    {"name": "誓约之盾", "description": "向敌人发起冲锋并造成沉默", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
                    {"name": "回旋打击", "description": "召唤圣盾围绕自身旋转，对周围敌人造成伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
                    {"name": "圣剑裁决", "description": "跃向空中后砸向地面，造成高额物理伤害", "cooldown": "42秒", "cost": "100法力", "type": "大招"}
                ],
                "passive_skill": {"name": "圣光守护", "description": "每2秒对周围的敌人造成基于自身生命值的法术伤害"},
                "win_rate": 0.50,
                "ban_rate": 0.02,
                "pick_rate": 0.40,
                "counter_heroes": ["典韦", "程咬金", "吕布"],
                "countered_by_heroes": ["马可波罗", "嬴政", "不知火舞"],
                "version": "1.0.0"
            },
            {
                "name": "妲己",
                "title": "绝代智谋",
                "position": "mage",
                "difficulty": "easy",
                "description": "妲己是法师英雄的代表，技能简单易上手，爆发能力强。",
                "skills": [
                    {"name": "灵魂冲击", "description": "向前方释放一道灵魂波，造成法术伤害并减少敌人移动速度", "cooldown": "10秒", "cost": "70法力", "type": "主动技能"},
                    {"name": "偶像魅力", "description": "对指定敌人造成法术伤害并眩晕", "cooldown": "12秒", "cost": "90法力", "type": "主动技能"},
                    {"name": "女王崇拜", "description": "召唤大批火蜂攻击范围内的敌人", "cooldown": "18秒", "cost": "120法力", "type": "大招"}
                ],
                "passive_skill": {"name": "失心", "description": "技能命中会减少目标法术防御"},
                "win_rate": 0.51,
                "ban_rate": 0.03,
                "pick_rate": 0.38,
                "counter_heroes": ["安琪拉", "王昭君", "甄姬"],
                "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
                "version": "1.0.0"
            },
            {
                "name": "孙悟空",
                "title": "齐天大圣",
                "position": "assassin",
                "difficulty": "medium",
                "description": "孙悟空是高爆发刺客英雄，擅长突进和击杀脆皮英雄。",
                "skills": [
                    {"name": "护身咒法", "description": "使用护身咒法抵挡一次技能并获得加速", "cooldown": "12秒", "cost": "无消耗", "type": "主动技能"},
                    {"name": "斗战冲锋", "description": "向指定方向冲锋，对路径上的敌人造成伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
                    {"name": "如意金箍", "description": "将金箍棒变大并向指定方向砸去，造成高额物理伤害", "cooldown": "40秒", "cost": "100法力", "type": "大招"}
                ],
                "passive_skill": {"name": "大圣神威", "description": "每次释放技能后强化下一次普攻"},
                "win_rate": 0.53,
                "ban_rate": 0.08,
                "pick_rate": 0.30,
                "counter_heroes": ["后羿", "鲁班七号", "妲己"],
                "countered_by_heroes": ["东皇太一", "张良", "武则天"],
                "version": "1.0.0"
            },
            {
                "name": "张飞",
                "title": "破胆之吼",
                "position": "support",
                "difficulty": "medium",
                "description": "张飞是强力辅助英雄，能为队友提供保护和控制。",
                "skills": [
                    {"name": "画地为牢", "description": "在指定区域形成障碍，敌人无法穿越", "cooldown": "12秒", "cost": "80法力", "type": "主动技能"},
                    {"name": "狂兽血性", "description": "进入狂暴状态，增加攻击力和攻击范围", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
                    {"name": "崩山裂地", "description": "跳向指定区域并怒吼，造成物理伤害并击飞敌人", "cooldown": "50秒", "cost": "100法力", "type": "大招"}
                ],
                "passive_skill": {"name": "狂意", "description": "普通攻击和技能命中会积攒怒气"},
                "win_rate": 0.54,
                "ban_rate": 0.06,
                "pick_rate": 0.25,
                "counter_heroes": ["孙悟空", "韩信", "阿轲"],
                "countered_by_heroes": ["吕布", "貂蝉", "马可波罗"],
                "version": "1.0.0"
            },
            {
                "name": "程咬金",
                "title": "霸道之气",
                "position": "tank",
                "difficulty": "easy",
                "description": "程咬金是坦克英雄，拥有强大的生存能力和持续输出能力。",
                "skills": [
                    {"name": "爆裂双斧", "description": "向指定方向投掷双斧，造成物理伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
                    {"name": "激怒", "description": "消耗自身生命值增加攻击力和移动速度", "cooldown": "10秒", "cost": "生命值", "type": "主动技能"},
                    {"name": "正义潜能", "description": "回复大量生命值并增加移动速度", "cooldown": "40秒", "cost": "生命值", "type": "大招"}
                ],
                "passive_skill": {"name": "舍身", "description": "每损失1%生命值额外获得攻击力加成"},
                "win_rate": 0.51,
                "ban_rate": 0.02,
                "pick_rate": 0.20,
                "counter_heroes": ["鲁班七号", "后羿", "马可波罗"],
                "countered_by_heroes": ["典韦", "吕布", "关羽"],
                "version": "1.0.0"
            }
        ]
        
        for hero_data in sample_heroes:
            hero = Hero(**hero_data)
            db.add(hero)
            
            equipment = HeroEquipment(
                hero_id=hero.id,
                rank="全部",
                position=hero.position,
                equipment_list=[
                    {"name": "急速战靴", "price": 710},
                    {"name": "末世", "price": 2160},
                    {"name": "无尽战刃", "price": 2140},
                    {"name": "破晓", "price": 3400},
                    {"name": "泣血之刃", "price": 1740},
                    {"name": "破军", "price": 2950}
                ] if hero.position == "archer" else [
                    {"name": "抵抗之靴", "price": 710},
                    {"name": "暗影战斧", "price": 2190},
                    {"name": "冰痕之握", "price": 2100},
                    {"name": "不死鸟之眼", "price": 2100},
                    {"name": "霸者重装", "price": 2070},
                    {"name": "贤者的庇护", "price": 2080}
                ],
                win_rate=0.55,
                pick_rate=0.45,
                version="1.0.0"
            )
            db.add(equipment)
            
            inscription = HeroInscription(
                hero_id=hero.id,
                rank="全部",
                inscription_name="通用搭配",
                inscription_config={
                    "red": {"name": "祸源", "count": 10},
                    "blue": {"name": "鹰眼", "count": 10},
                    "green": {"name": "狩猎", "count": 10}
                },
                description="适合大多数情况的通用铭文搭配",
                win_rate=0.53,
                version="1.0.0"
            )
            db.add(inscription)
        
        db.commit()
        print("示例数据初始化完成")
        
    except Exception as e:
        print(f"初始化数据时出错: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()
