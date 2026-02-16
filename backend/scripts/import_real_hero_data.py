import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.hero import Hero, HeroEquipment, HeroInscription, Equipment


REAL_HEROES = [
    {
        "name": "亚瑟",
        "title": "圣光之盾",
        "position": "warrior",
        "difficulty": "easy",
        "image_url": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/166/166.jpg",
        "description": "亚瑟是王者峡谷中非常均衡的战士，拥有强大的生存能力和持续的输出能力，适合新手玩家。",
        "skills": [
            {"name": "誓约之盾", "description": "亚瑟祝福圣盾，跳向目标造成物理伤害并沉默目标", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "回旋打击", "description": "亚瑟召唤圣盾围绕自身旋转，对周围的敌人造成持续伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "圣剑裁决", "description": "亚瑟跃向空中，落地时造成高额物理伤害并击飞敌人", "cooldown": "42秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "圣光守护", "description": "亚瑟每2秒对周围的敌人造成基于自身生命值的法术伤害"},
        "win_rate": 0.51,
        "ban_rate": 0.02,
        "pick_rate": 0.40,
        "counter_heroes": ["典韦", "程咬金", "吕布"],
        "countered_by_heroes": ["马可波罗", "嬴政", "不知火舞"],
        "version": "1.0.0"
    },
    {
        "name": "鲁班七号",
        "title": "鲁班大师号机关造物",
        "position": "archer",
        "difficulty": "easy",
        "description": "鲁班七号是鲁班大师发明的高智能机关造物，拥有极高的射击天赋，是射手英雄中的热门选择。",
        "skills": [
            {"name": "火力压制", "description": "向指定方向扫射，对范围内的敌人造成物理伤害", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "无敌鲨嘴炮", "description": "向指定方向发射炮弹，对路径上的敌人造成物理伤害", "cooldown": "12秒", "cost": "50法力", "type": "主动技能"},
            {"name": "空中支援", "description": "召唤河豚飞艇对指定区域进行火力打击，造成高额物理伤害", "cooldown": "36秒", "cost": "100法力", "type": "大招"}
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
        "name": "妲己",
        "title": "绝代智谋",
        "position": "mage",
        "difficulty": "easy",
        "description": "妲己是法师英雄的代表，技能简单易上手，爆发能力强，是中单的热门选择。",
        "skills": [
            {"name": "灵魂冲击", "description": "妲己向前方释放一道灵魂波，对命中的敌人造成法术伤害并减少其移动速度", "cooldown": "10秒", "cost": "70法力", "type": "主动技能"},
            {"name": "偶像魅力", "description": "妲己对指定敌人释放魅力，造成法术伤害并眩晕目标", "cooldown": "12秒", "cost": "90法力", "type": "主动技能"},
            {"name": "女王崇拜", "description": "妲己召唤大批火蜂攻击范围内的敌人，造成高额法术伤害", "cooldown": "18秒", "cost": "120法力", "type": "大招"}
        ],
        "passive_skill": {"name": "失心", "description": "妲己的技能命中会减少目标的法术防御"},
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
        "description": "孙悟空是高爆发刺客英雄，擅长突进和击杀脆皮英雄，是打野的热门选择。",
        "skills": [
            {"name": "护身咒法", "description": "孙悟空使用护身咒法抵挡一次技能并获得加速", "cooldown": "12秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "斗战冲锋", "description": "孙悟空向指定方向冲锋，对路径上的敌人造成伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "如意金箍", "description": "孙悟空将金箍棒变大并向指定方向砸去，造成高额物理伤害", "cooldown": "40秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "大圣神威", "description": "孙悟空每次释放技能后强化下一次普攻"},
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
        "description": "张飞是强力辅助英雄，能为队友提供保护和控制，是辅助的热门选择。",
        "skills": [
            {"name": "画地为牢", "description": "张飞在指定区域形成障碍，敌人无法穿越", "cooldown": "12秒", "cost": "80法力", "type": "主动技能"},
            {"name": "狂兽血性", "description": "张飞进入狂暴状态，增加攻击力和攻击范围", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "崩山裂地", "description": "张飞跳向指定区域并怒吼，造成物理伤害并击飞敌人", "cooldown": "50秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "狂意", "description": "张飞普通攻击和技能命中会积攒怒气"},
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
        "description": "程咬金是坦克英雄，拥有强大的生存能力和持续输出能力，是上单的热门选择。",
        "skills": [
            {"name": "爆裂双斧", "description": "程咬金向指定方向投掷双斧，对命中的敌人造成物理伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "激怒", "description": "程咬金消耗自身生命值增加攻击力和移动速度", "cooldown": "10秒", "cost": "生命值", "type": "主动技能"},
            {"name": "正义潜能", "description": "程咬金回复大量生命值并增加移动速度", "cooldown": "40秒", "cost": "生命值", "type": "大招"}
        ],
        "passive_skill": {"name": "舍身", "description": "程咬金每损失1%生命值额外获得攻击力加成"},
        "win_rate": 0.51,
        "ban_rate": 0.02,
        "pick_rate": 0.20,
        "counter_heroes": ["鲁班七号", "后羿", "马可波罗"],
        "countered_by_heroes": ["典韦", "吕布", "关羽"],
        "version": "1.0.0"
    },
    {
        "name": "后羿",
        "title": "射落九日",
        "position": "archer",
        "difficulty": "easy",
        "description": "后羿是远程物理输出英雄，拥有强大的远程攻击能力，是射手的热门选择。",
        "skills": [
            {"name": "多重箭矢", "description": "后羿向前方发射多支箭矢，对命中的敌人造成物理伤害", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "落日余晖", "description": "后羿召唤落日之力，对指定区域的敌人造成物理伤害", "cooldown": "12秒", "cost": "50法力", "type": "主动技能"},
            {"name": "灼日之矢", "description": "后羿向指定方向发射灼日之矢，造成高额物理伤害并击飞敌人", "cooldown": "36秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "惩戒射击", "description": "后羿的普攻命中会叠加层数，达到一定层数后触发额外伤害"},
        "win_rate": 0.51,
        "ban_rate": 0.04,
        "pick_rate": 0.32,
        "counter_heroes": ["典韦", "程咬金", "张飞"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    },
    {
        "name": "安琪拉",
        "title": "萝莉法师",
        "position": "mage",
        "difficulty": "easy",
        "description": "安琪拉是法师英雄，拥有强大的法术伤害能力，是中单的热门选择。",
        "skills": [
            {"name": "火球术", "description": "安琪拉向前方发射火球，对命中的敌人造成法术伤害", "cooldown": "10秒", "cost": "70法力", "type": "主动技能"},
            {"name": "混沌火种", "description": "安琪拉在指定位置种下火种，对敌人造成法术伤害并减速", "cooldown": "12秒", "cost": "90法力", "type": "主动技能"},
            {"name": "炽热光辉", "description": "安琪拉释放炽热光辉，对范围内的敌人造成高额法术伤害", "cooldown": "18秒", "cost": "120法力", "type": "大招"}
        ],
        "passive_skill": {"name": "咒术火焰", "description": "安琪拉的技能命中会减少目标的法术防御"},
        "win_rate": 0.52,
        "ban_rate": 0.03,
        "pick_rate": 0.35,
        "counter_heroes": ["妲己", "王昭君", "甄姬"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    },
    {
        "name": "韩信",
        "title": "国士无双",
        "position": "assassin",
        "difficulty": "hard",
        "description": "韩信是高机动性刺客英雄，拥有极强的突进和逃生能力，是打野的高端选择。",
        "skills": [
            {"name": "无情冲锋", "description": "韩信向指定方向冲锋，对命中的敌人造成物理伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "背水一战", "description": "韩信激活背水一战，增加攻击力和攻击速度", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "国士无双", "description": "韩信释放国士无双，对范围内的敌人造成高额物理伤害", "cooldown": "40秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "杀意之枪", "description": "韩信第四次普攻会将敌人击飞"},
        "win_rate": 0.50,
        "ban_rate": 0.07,
        "pick_rate": 0.18,
        "counter_heroes": ["鲁班七号", "后羿", "妲己"],
        "countered_by_heroes": ["东皇太一", "张良", "盾山"],
        "version": "1.0.0"
    },
    {
        "name": "貂蝉",
        "title": "绝世舞姬",
        "position": "mage",
        "difficulty": "hard",
        "description": "貂蝉是高机动性法师英雄，拥有强大的持续输出和生存能力，是中高端选择。",
        "skills": [
            {"name": "落·红莲", "description": "貂蝉在指定位置释放红莲，对敌人造成法术伤害", "cooldown": "10秒", "cost": "70法力", "type": "主动技能"},
            {"name": "缘·心结", "description": "貂蝉释放缘·心结，对敌人造成法术伤害并减速", "cooldown": "12秒", "cost": "90法力", "type": "主动技能"},
            {"name": "绽·风华", "description": "貂蝉释放绽·风华，对范围内的敌人造成高额法术伤害", "cooldown": "18秒", "cost": "120法力", "type": "大招"}
        ],
        "passive_skill": {"name": "花语", "description": "貂蝉的技能命中会减少技能冷却时间"},
        "win_rate": 0.53,
        "ban_rate": 0.05,
        "pick_rate": 0.22,
        "counter_heroes": ["妲己", "安琪拉", "王昭君"],
        "countered_by_heroes": ["张良", "东皇太一", "金蝉"],
        "version": "1.0.0"
    },
    {
        "name": "兰陵王",
        "title": "暗影刀锋",
        "position": "assassin",
        "difficulty": "medium",
        "description": "兰陵王是隐身刺客英雄，拥有强大的突进和击杀能力，是打野的热门选择。",
        "skills": [
            {"name": "秘技·影袭", "description": "兰陵王向指定方向突进，对命中的敌人造成物理伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "秘技·影蚀", "description": "兰陵王进入隐身状态，增加移动速度", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "秘技·暗袭", "description": "兰陵王释放暗袭，对范围内的敌人造成高额物理伤害", "cooldown": "40秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "暗影", "description": "兰陵王接近敌方英雄时会获得加速"},
        "win_rate": 0.52,
        "ban_rate": 0.06,
        "pick_rate": 0.25,
        "counter_heroes": ["鲁班七号", "后羿", "妲己"],
        "countered_by_heroes": ["东皇太一", "张良", "典韦"],
        "version": "1.0.0"
    },
    {
        "name": "阿轲",
        "title": "刹那芳华",
        "position": "assassin",
        "difficulty": "hard",
        "description": "阿轲是高爆发刺客英雄，拥有强大的击杀和收割能力，是打野的高端选择。",
        "skills": [
            {"name": "弧光", "description": "阿轲向指定方向释放弧光，对命中的敌人造成物理伤害", "cooldown": "8秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "幻舞", "description": "阿轲进入幻舞状态，增加攻击力和移动速度", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "刹那", "description": "阿轲释放刹那，对范围内的敌人造成高额物理伤害", "cooldown": "40秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "死吻", "description": "阿轲击杀或助攻后重置技能冷却时间"},
        "win_rate": 0.51,
        "ban_rate": 0.07,
        "pick_rate": 0.20,
        "counter_heroes": ["鲁班七号", "后羿", "妲己"],
        "countered_by_heroes": ["东皇太一", "张良", "典韦"],
        "version": "1.0.0"
    },
    {
        "name": "王昭君",
        "title": "冰雪之华",
        "position": "mage",
        "difficulty": "medium",
        "description": "王昭君是控制型法师英雄，拥有强大的控制能力和范围伤害，是中单的热门选择。",
        "skills": [
            {"name": "冰封", "description": "王昭君在指定位置释放冰封，对敌人造成法术伤害并冻结", "cooldown": "10秒", "cost": "70法力", "type": "主动技能"},
            {"name": "冰雪", "description": "王昭君释放冰雪，对敌人造成法术伤害并减速", "cooldown": "12秒", "cost": "90法力", "type": "主动技能"},
            {"name": "凛冬", "description": "王昭君释放凛冬，对范围内的敌人造成高额法术伤害并冻结", "cooldown": "18秒", "cost": "120法力", "type": "大招"}
        ],
        "passive_skill": {"name": "冰心", "description": "王昭君的技能命中会减少敌人的移动速度"},
        "win_rate": 0.51,
        "ban_rate": 0.04,
        "pick_rate": 0.28,
        "counter_heroes": ["妲己", "安琪拉", "甄姬"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    },
    {
        "name": "甄姬",
        "title": "洛神降临",
        "position": "mage",
        "difficulty": "easy",
        "description": "甄姬是控制型法师英雄，拥有强大的控制能力和范围伤害，是中单的热门选择。",
        "skills": [
            {"name": "泪如泉涌", "description": "甄姬向前方释放泪如泉涌，对命中的敌人造成法术伤害", "cooldown": "10秒", "cost": "70法力", "type": "主动技能"},
            {"name": "叹息水流", "description": "甄姬释放叹息水流，对敌人造成法术伤害并减速", "cooldown": "12秒", "cost": "90法力", "type": "主动技能"},
            {"name": "洛神降临", "description": "甄姬释放洛神降临，对范围内的敌人造成高额法术伤害并冻结", "cooldown": "18秒", "cost": "120法力", "type": "大招"}
        ],
        "passive_skill": {"name": "凝泪成冰", "description": "甄姬的技能命中会叠加层数，达到一定层数后冻结敌人"},
        "win_rate": 0.50,
        "ban_rate": 0.03,
        "pick_rate": 0.30,
        "counter_heroes": ["妲己", "安琪拉", "王昭君"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    },
    {
        "name": "马可波罗",
        "title": "远游之枪",
        "position": "archer",
        "difficulty": "medium",
        "description": "马可波罗是高机动性射手英雄，拥有强大的远程攻击能力，是射手的热门选择。",
        "skills": [
            {"name": "华丽左轮", "description": "马可波罗向指定方向发射华丽左轮，对命中的敌人造成物理伤害", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "漫游之枪", "description": "马可波罗释放漫游之枪，增加攻击速度和移动速度", "cooldown": "12秒", "cost": "50法力", "type": "主动技能"},
            {"name": "绯红弹幕", "description": "马可波罗释放绯红弹幕，对范围内的敌人造成高额物理伤害", "cooldown": "36秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "连锁反应", "description": "马可波罗的普攻命中会触发连锁反应，对多个目标造成伤害"},
        "win_rate": 0.52,
        "ban_rate": 0.05,
        "pick_rate": 0.27,
        "counter_heroes": ["张飞", "程咬金", "典韦"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    },
    {
        "name": "虞姬",
        "title": "森之心",
        "position": "archer",
        "difficulty": "easy",
        "description": "虞姬是远程物理输出英雄，拥有强大的远程攻击能力，是射手的热门选择。",
        "skills": [
            {"name": "楚歌起舞", "description": "虞姬向前方释放楚歌起舞，对命中的敌人造成物理伤害", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "大树来仪", "description": "虞姬释放大树来仪，对指定区域的敌人造成物理伤害", "cooldown": "12秒", "cost": "50法力", "type": "主动技能"},
            {"name": "阵前舞", "description": "虞姬释放阵前舞，对范围内的敌人造成高额物理伤害", "cooldown": "36秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "神树庇佑", "description": "虞姬的普攻命中会减少目标的移动速度"},
        "win_rate": 0.50,
        "ban_rate": 0.03,
        "pick_rate": 0.25,
        "counter_heroes": ["张飞", "程咬金", "典韦"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    },
    {
        "name": "百里守约",
        "title": "静谧之眼",
        "position": "archer",
        "difficulty": "medium",
        "description": "百里守约是远程狙击型射手英雄，拥有强大的远程攻击能力，是射手的高端选择。",
        "skills": [
            {"name": "静谧之眼", "description": "百里守约在指定位置放置静谧之眼，提供视野", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "伏击", "description": "百里守约进入伏击状态，增加攻击力和暴击率", "cooldown": "12秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "完美狙击", "description": "百里守约释放完美狙击，对指定敌人造成高额物理伤害", "cooldown": "36秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "瞄准", "description": "百里守约的普攻和技能命中会降低敌人的视野"},
        "win_rate": 0.49,
        "ban_rate": 0.04,
        "pick_rate": 0.22,
        "counter_heroes": ["张飞", "程咬金", "典韦"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    },
    {
        "name": "伽罗",
        "title": "长弓破风",
        "position": "archer",
        "difficulty": "medium",
        "description": "伽罗是远程物理输出英雄，拥有强大的远程攻击能力，是射手的热门选择。",
        "skills": [
            {"name": "长弓破风", "description": "伽罗向指定方向释放长弓破风，对命中的敌人造成物理伤害", "cooldown": "10秒", "cost": "无消耗", "type": "主动技能"},
            {"name": "轻语", "description": "伽罗释放轻语，增加攻击速度和移动速度", "cooldown": "12秒", "cost": "50法力", "type": "主动技能"},
            {"name": "纯净之域", "description": "伽罗释放纯净之域，对范围内的敌人造成高额物理伤害", "cooldown": "36秒", "cost": "100法力", "type": "大招"}
        ],
        "passive_skill": {"name": "破甲", "description": "伽罗的普攻和技能命中会减少敌人的护甲"},
        "win_rate": 0.51,
        "ban_rate": 0.04,
        "pick_rate": 0.24,
        "counter_heroes": ["张飞", "程咬金", "典韦"],
        "countered_by_heroes": ["兰陵王", "阿轲", "孙悟空"],
        "version": "1.0.0"
    }
]

EQUIPMENT_DATA = {
    "archer": [
        {"name": "急速战靴", "price": 710, "type": "移动装备", "stats": {"移动速度": 60}},
        {"name": "末世", "price": 2160, "type": "攻击装备", "stats": {"物理攻击": 60, "攻击速度": 10}},
        {"name": "无尽战刃", "price": 2140, "type": "攻击装备", "stats": {"物理攻击": 120, "暴击率": 20}},
        {"name": "破晓", "price": 3400, "type": "攻击装备", "stats": {"物理攻击": 50, "攻击速度": 35, "物理穿透": 40}},
        {"name": "泣血之刃", "price": 1740, "type": "攻击装备", "stats": {"物理攻击": 100, "物理吸血": 25}},
        {"name": "破军", "price": 2950, "type": "攻击装备", "stats": {"物理攻击": 180}}
    ],
    "warrior": [
        {"name": "抵抗之靴", "price": 710, "type": "移动装备", "stats": {"移动速度": 60, "韧性": 110}},
        {"name": "暗影战斧", "price": 2190, "type": "攻击装备", "stats": {"物理攻击": 85, "冷却缩减": 15, "生命值": 500}},
        {"name": "冰痕之握", "price": 2100, "type": "防御装备", "stats": {"物理防御": 200, "生命值": 800, "冷却缩减": 10}},
        {"name": "不死鸟之眼", "price": 2100, "type": "防御装备", "stats": {"法术防御": 240, "生命值": 1000}},
        {"name": "霸者重装", "price": 2070, "type": "防御装备", "stats": {"生命值": 2000, "每秒回血": 100}},
        {"name": "贤者的庇护", "price": 2080, "type": "防御装备", "stats": {"物理防御": 140, "法术防御": 140}}
    ],
    "mage": [
        {"name": "冷静之靴", "price": 710, "type": "移动装备", "stats": {"移动速度": 60, "冷却缩减": 15}},
        {"name": "回响之杖", "price": 2100, "type": "法术装备", "stats": {"法术攻击": 240, "冷却缩减": 7}},
        {"name": "博学者之怒", "price": 2700, "type": "法术装备", "stats": {"法术攻击": 500, "冷却缩减": 20}},
        {"name": "虚无法杖", "price": 2750, "type": "法术装备", "stats": {"法术攻击": 300, "法术穿透": 40}},
        {"name": "辉月", "price": 1990, "type": "法术装备", "stats": {"法术攻击": 180, "冷却缩减": 20}},
        {"name": "贤者之书", "price": 2950, "type": "法术装备", "stats": {"法术攻击": 400, "最大法力": 500}}
    ],
    "assassin": [
        {"name": "追击刀锋", "price": 710, "type": "移动装备", "stats": {"移动速度": 60, "物理攻击": 15}},
        {"name": "暗影战斧", "price": 2190, "type": "攻击装备", "stats": {"物理攻击": 85, "冷却缩减": 15, "生命值": 500}},
        {"name": "宗师之力", "price": 2100, "type": "攻击装备", "stats": {"物理攻击": 80, "暴击率": 20}},
        {"name": "破军", "price": 2950, "type": "攻击装备", "stats": {"物理攻击": 180}},
        {"name": "泣血之刃", "price": 1740, "type": "攻击装备", "stats": {"物理攻击": 100, "物理吸血": 25}},
        {"name": "名刀", "price": 1800, "type": "攻击装备", "stats": {"物理攻击": 60, "冷却缩减": 10}}
    ],
    "tank": [
        {"name": "抵抗之靴", "price": 710, "type": "移动装备", "stats": {"移动速度": 60, "韧性": 110}},
        {"name": "不祥征兆", "price": 2180, "type": "防御装备", "stats": {"物理防御": 270, "生命值": 1200}},
        {"name": "魔女斗篷", "price": 2120, "type": "防御装备", "stats": {"法术防御": 360, "生命值": 1000}},
        {"name": "霸者重装", "price": 2070, "type": "防御装备", "stats": {"生命值": 2000, "每秒回血": 100}},
        {"name": "贤者的庇护", "price": 2080, "type": "防御装备", "stats": {"物理防御": 140, "法术防御": 140}},
        {"name": "复活甲", "price": 2080, "type": "防御装备", "stats": {"物理防御": 140, "法术防御": 140}}
    ],
    "support": [
        {"name": "疾步之靴", "price": 710, "type": "移动装备", "stats": {"移动速度": 60, "回蓝": 500}},
        {"name": "极影", "price": 1900, "type": "辅助装备", "stats": {"冷却缩减": 10, "移动速度": 5}},
        {"name": "近卫荣耀", "price": 1900, "type": "辅助装备", "stats": {"生命值": 500, "回血": 10}},
        {"name": "救赎之翼", "price": 1800, "type": "辅助装备", "stats": {"生命值": 500, "冷却缩减": 10}},
        {"name": "星泉", "price": 1750, "type": "辅助装备", "stats": {"回蓝": 500, "回血": 50}},
        {"name": "奔狼纹章", "price": 1800, "type": "辅助装备", "stats": {"冷却缩减": 10, "移动速度": 5}}
    ]
}

INSCRIPTION_DATA = {
    "archer": [
        {"name": "10祸源 10鹰眼 10狩猎", "description": "提供16%暴击率、9点物理攻击、10%移速和10%攻速，适合射手英雄"},
        {"name": "10无双 10鹰眼 10夺萃", "description": "提供36%暴击效果、9点物理攻击、16%物理吸血，适合射手英雄"}
    ],
    "warrior": [
        {"name": "10异变 10鹰眼 10狩猎", "description": "提供41物理穿透、9点物理攻击、10%移速和10%攻速，适合战士英雄"},
        {"name": "10祸源 10鹰眼 10隐匿", "description": "提供16%暴击率、9点物理攻击、16物理攻击和10%移速，适合战士英雄"}
    ],
    "mage": [
        {"name": "10梦魇 10心眼 10狩猎", "description": "提供42法术穿透、64法术攻击、10%移速和10%攻速，适合法师英雄"},
        {"name": "10梦魇 10心眼 10贪婪", "description": "提供42法术穿透、64法术攻击、16法术吸血，适合法师英雄"}
    ],
    "assassin": [
        {"name": "10异变 10鹰眼 10隐匿", "description": "提供41物理穿透、9点物理攻击、16物理攻击和10%移速，适合刺客英雄"},
        {"name": "10无双 10鹰眼 10夺萃", "description": "提供36%暴击效果、9点物理攻击、16%物理吸血，适合刺客英雄"}
    ],
    "tank": [
        {"name": "10宿命 10虚空 10调和", "description": "提供337最大生命、23物理防御、每5秒回血52和每5秒回蓝31，适合坦克英雄"},
        {"name": "10长生 10虚空 10调和", "description": "提供375最大生命、23物理防御、每5秒回血52和每5秒回蓝31，适合坦克英雄"}
    ],
    "support": [
        {"name": "10宿命 10虚空 10调和", "description": "提供337最大生命、23物理防御、每5秒回血52和每5秒回蓝31，适合辅助英雄"},
        {"name": "10圣人 10怜悯 10狩猎", "description": "提供53法术攻击、10冷却缩减、10%移速和10%攻速，适合辅助英雄"}
    ]
}


def import_heroes(db: Session):
    print("开始导入英雄数据...")
    
    existing_heroes = db.query(Hero).all()
    existing_names = {hero.name for hero in existing_heroes}
    
    imported_count = 0
    heroes_to_add = []
    for hero_data in REAL_HEROES:
        if hero_data["name"] not in existing_names:
            hero = Hero(**hero_data)
            db.add(hero)
            heroes_to_add.append((hero, hero_data))
            imported_count += 1
    
    db.flush()
    db.commit()
    
    for hero, hero_data in heroes_to_add:
        equipment_list = EQUIPMENT_DATA.get(hero_data["position"], [])
        for eq_data in equipment_list:
            equipment = HeroEquipment(
                hero_id=hero.id,
                rank="全部",
                position=hero_data["position"],
                equipment_list=[eq_data],
                win_rate=0.55,
                pick_rate=0.45,
                version="1.0.0"
            )
            db.add(equipment)
        
        inscription_list = INSCRIPTION_DATA.get(hero_data["position"], [])
        for insc_data in inscription_list:
            inscription = HeroInscription(
                hero_id=hero.id,
                rank="全部",
                inscription_name=insc_data["name"].split()[0],
                inscription_config={"name": insc_data["name"]},
                description=insc_data["description"],
                win_rate=0.53,
                version="1.0.0"
            )
            db.add(inscription)
    
    db.commit()
    print(f"导入完成！新增 {imported_count} 个英雄")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        import_heroes(db)
        print("英雄数据导入成功！")
    except Exception as e:
        print(f"导入失败：{e}")
        db.rollback()
    finally:
        db.close()
