import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.hero import Hero

HERO_IMAGES = {
    "亚瑟": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/166/166.jpg",
    "鲁班七号": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/112/112.jpg",
    "妲己": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/109/109.jpg",
    "孙悟空": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/167/167.jpg",
    "张飞": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/194/194.jpg",
    "程咬金": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/195/195.jpg",
    "后羿": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/169/169.jpg",
    "安琪拉": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/142/142.jpg",
    "韩信": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/198/198.jpg",
    "貂蝉": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/141/141.jpg",
    "兰陵王": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/171/171.jpg",
    "阿轲": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/116/116.jpg",
    "王昭君": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/152/152.jpg",
    "甄姬": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/127/127.jpg",
    "马可波罗": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/502/502.jpg",
    "虞姬": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/508/508.jpg",
    "百里守约": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/501/501.jpg",
    "伽罗": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/507/507.jpg"
}


def update_hero_images(db: Session):
    print("开始更新英雄图片...")
    
    heroes = db.query(Hero).all()
    updated_count = 0
    
    for hero in heroes:
        if hero.name in HERO_IMAGES:
            hero.image_url = HERO_IMAGES[hero.name]
            updated_count += 1
            print(f"✓ 更新 {hero.name} 的图片")
        else:
            print(f"✗ 未找到 {hero.name} 的图片")
    
    db.commit()
    print(f"\n更新完成！共更新 {updated_count} 个英雄的图片")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        update_hero_images(db)
        print("英雄图片更新成功！")
    except Exception as e:
        print(f"更新失败：{e}")
        db.rollback()
    finally:
        db.close()
