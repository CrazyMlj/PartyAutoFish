from enum import Enum


def get_all_fish_rod_type_name():
    names = []
    for e in FishRodType:
        names.append(e.value[0])
    return names


class FishRodType(Enum):
    """鱼竿类型枚举"""
    ULTRALIGHT_LURE = ('路亚轻杆', 'ul')  # 路亚轻杆
    HEAVY_LURE = ('路亚重杆', 'hl')  # 路亚重杆
    ULTRALIGHT_ICE = ('冰钓轻杆', 'ui')  # 冰钓轻杆
    HEAVY_ICE = ('冰钓重杆', 'hi')  # 冰钓重杆
    ULTRALIGHT_SPRING = ('春钓轻杆', 'us')  # 春钓轻杆
    HEAVY_SPRING = ('春钓重杆', 'hs')  # 春钓重杆

    @classmethod
    def from_string(cls, name: str) -> 'FishRodType':
        """从字符串创建枚举"""
        name_map = {
            '路亚轻杆': cls.ULTRALIGHT_LURE, 'ul': cls.ULTRALIGHT_LURE,
            '路亚重杆': cls.HEAVY_LURE, 'hl': cls.HEAVY_LURE,
            '冰钓轻杆': cls.ULTRALIGHT_ICE, 'ui': cls.ULTRALIGHT_ICE,
            '冰钓重杆': cls.HEAVY_ICE, 'hi': cls.HEAVY_ICE,
            '春钓轻杆': cls.ULTRALIGHT_SPRING, 'us': cls.ULTRALIGHT_SPRING,
            '春钓重杆': cls.HEAVY_SPRING, 'hs': cls.HEAVY_SPRING
        }
        return name_map.get(name.lower(), cls.HEAVY_LURE)
