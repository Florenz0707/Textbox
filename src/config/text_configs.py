from __future__ import annotations

# 角色左上角“姓名部件”装饰字配置
text_configs_dict: dict[str, list[dict]] = {
    "nanoka": [  # 黑部奈叶香
        {"text": "黑", "position": (759, 63), "font_color": (131, 143, 147), "font_size": 196},
        {"text": "部", "position": (955, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "奈", "position": (1053, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "叶香", "position": (1197, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "hiro": [  # 二阶堂希罗
        {"text": "二", "position": (759, 63), "font_color": (239, 79, 84), "font_size": 196},
        {"text": "阶堂", "position": (955, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "希", "position": (1143, 110), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "罗", "position": (1283, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "ema": [  # 樱羽艾玛
        {"text": "樱", "position": (759, 73), "font_color": (253, 145, 175), "font_size": 186},
        {"text": "羽", "position": (949, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "艾", "position": (1039, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "玛", "position": (1183, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "sherri": [  # 橘雪莉
        {"text": "橘", "position": (759, 73), "font_color": (137, 177, 251), "font_size": 186},
        {"text": "雪", "position": (943, 110), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "莉", "position": (1093, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1}
    ],
    "anan": [  # 夏目安安
        {"text": "夏", "position": (759, 73), "font_color": (159, 145, 251), "font_size": 186},
        {"text": "目", "position": (949, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "安", "position": (1039, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "安", "position": (1183, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "noa": [  # 城崎诺亚
        {"text": "城", "position": (759, 73), "font_color": (104, 223, 231), "font_size": 186},
        {"text": "崎", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "诺", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "亚", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "coco": [  # 泽渡可可
        {"text": "泽", "position": (759, 73), "font_color": (251, 114, 78), "font_size": 186},
        {"text": "渡", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "可", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "可", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "alisa": [  # 紫藤亚里沙
        {"text": "紫", "position": (759, 73), "font_color": (235, 75, 60), "font_size": 186},
        {"text": "藤", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "亚", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "里沙", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "reia": [  # 莲见蕾雅
        {"text": "莲", "position": (759, 73), "font_color": (253, 177, 88), "font_size": 186},
        {"text": "见", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "蕾", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "雅", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "mago": [  # 宝生玛格
        {"text": "宝", "position": (759, 73), "font_color": (185, 124, 235), "font_size": 186},
        {"text": "生", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "玛", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "格", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "hanna": [  # 远野汉娜
        {"text": "远", "position": (759, 73), "font_color": (169, 199, 30), "font_size": 186},
        {"text": "野", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "汉", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "娜", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "meruru": [  # 冰上梅露露
        {"text": "冰", "position": (759, 73), "font_color": (227, 185, 175), "font_size": 186},
        {"text": "上", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "梅", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "露露", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "miria": [  # 佐伯米莉亚
        {"text": "佐", "position": (759, 73), "font_color": (235, 207, 139), "font_size": 186},
        {"text": "伯", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "米", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "莉亚", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
    "yuki": [  # 月代雪
        {"text": "月", "position": (759, 63), "font_color": (195, 209, 231), "font_size": 196},
        {"text": "代", "position": (948, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "雪", "position": (1053, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "", "position": (0, 0), "font_color": (255, 255, 255), "font_size": 1}
    ],
    "momoi": [
        {"text": "才", "position": (759, 73), "font_color": (255, 105, 80), "font_size": 186},
        {"text": "羽", "position": (945, 175), "font_color": (255, 255, 255), "font_size": 92},
        {"text": "桃", "position": (1042, 117), "font_color": (255, 255, 255), "font_size": 147},
        {"text": "井", "position": (1186, 175), "font_color": (255, 255, 255), "font_size": 92}
    ],
}
