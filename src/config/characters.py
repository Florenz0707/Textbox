from __future__ import annotations

# 角色配置字典
# 字体文件名对应 resource/font 目录
characters: dict[str, dict] = {
    "ema": {"emotion_count": 8, "font": "font3.ttf"},  # 樱羽艾玛
    "hiro": {"emotion_count": 6, "font": "font3.ttf"},  # 二阶堂希罗
    "sherri": {"emotion_count": 7, "font": "font3.ttf"},  # 橘雪莉
    "hanna": {"emotion_count": 5, "font": "font3.ttf"},  # 远野汉娜
    "anan": {"emotion_count": 9, "font": "font3.ttf"},  # 夏目安安
    "yuki": {"emotion_count": 18, "font": "font3.ttf"},
    "meruru": {"emotion_count": 6, "font": "font3.ttf"},  # 冰上梅露露
    "noa": {"emotion_count": 6, "font": "font3.ttf"},  # 城崎诺亚
    "reia": {"emotion_count": 7, "font": "font3.ttf"},  # 莲见蕾雅
    "miria": {"emotion_count": 4, "font": "font3.ttf"},  # 佐伯米莉亚
    "nanoka": {"emotion_count": 5, "font": "font3.ttf"},  # 黑部奈叶香
    "mago": {"emotion_count": 5, "font": "font3.ttf"},  # 宝生玛格
    "alisa": {"emotion_count": 6, "font": "font3.ttf"},  # 紫藤亚里沙
    "coco": {"emotion_count": 5, "font": "font3.ttf"},
    "momoi": {"emotion_count": 7, "font": "font3.ttf"},  # 才羽桃井
}

# 顺序列表
character_list: list[str] = list(characters.keys())
