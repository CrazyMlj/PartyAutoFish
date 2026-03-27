from enum import Enum, auto


class AnchorType(Enum):
    """锚点类型枚举"""
    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    CENTER = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()

    @classmethod
    def from_string(cls, name: str) -> 'AnchorType':
        """从字符串创建枚举"""
        name_map = {
            'top_left': cls.TOP_LEFT, 'tl': cls.TOP_LEFT,
            'top_center': cls.TOP_CENTER, 'tc': cls.TOP_CENTER,
            'top_right': cls.TOP_RIGHT, 'tr': cls.TOP_RIGHT,
            'center': cls.CENTER, 'c': cls.CENTER,
            'bottom_left': cls.BOTTOM_LEFT, 'bl': cls.BOTTOM_LEFT,
            'bottom_center': cls.BOTTOM_CENTER, 'bc': cls.BOTTOM_CENTER,
            'bottom_right': cls.BOTTOM_RIGHT, 'br': cls.BOTTOM_RIGHT,
        }
        return name_map.get(name.lower(), cls.CENTER)
