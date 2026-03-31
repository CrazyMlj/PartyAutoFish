from AnchorType import AnchorType
from ScreenAdapt import scale_point_anchored, scale_corner_anchored, scale_cords_by_percentage, scale_cords_x

# 位置信息(基准"2k")
BAIT_REGION_BASE = (2318, 1296, 30, 22, 'br')  # 鱼饵数量区域  3440*1440(3198, 1296) 右下角锚定 1k(1739,972)
BAIT_CORP_LOCATION = (15, 22, 'br')  # 鱼饵数量基本裁剪大小
FISH_STAR_REGION_BASE = (1172, 165, 35, 32, 'tc')  # 上鱼星星 3440*1440(1613, 165) 1K(879 122)
F_1_REGION_BASE = (1100, 1329, 11, 20, 'bc')  # F1位置 3440*1440(1539, 1296) 1K(823,995)
F_2_REGION_BASE = (1212, 1329, 11, 20, 'bc')  # F2位置
WAITING_STRIKE_REGION_BASE = (1007, 1324, 30, 30, 'bc')  # 等待上鱼位置
DRAG_FISH_REGION_BASE = (1007, 1094, 30, 30, 'bc')  # 拉鱼位置
FISHING_REGION_BASE = (1146, 1316, 18, 22, 'bc')  # 上鱼鼠标右键图标

OVERTIME_REGION_BASE = (1244, 674, 27, 30, 'tc')  # 加时界面检测区域 1685 674
BTN_NO_JIASHI_BASE = (1172, 784, 'c')  # 不加时按钮 1575
BTN_YES_JIASHI_BASE = (1387, 784, 'c')  # 加时按钮

OPEN_FISH_BUCKET_BIT_BASE = -200  # 打开鱼桶鼠标移动
BUCKET_OPENED_REGION_BASE = (2145, 408, 35, 37, 'tr')  # 桶以打开 3440*1440(3021, 408) 1K(1605,306)
BUCKET_FULL_REGION_BASE = (1184, 434, 36, 38, 'tc')  # 鱼桶满了(满)
NO_BAIT_REGION_BASE = (1183, 434, 37, 36, 'tc')  # 没有鱼饵
BUCKET_LEFT_NUM_REGION_BASE = (2148, 457, 28, 21, 'tr')  # 鱼桶已装(48) 2176 478
BUCKET_EMPTY_REGION_BASE = (2111, 909, 35, 35, 'br')  # 鱼桶一条鱼也没有(空)
FISH_COLOR_INFO_LOCATION = (1924, 640, 'tr')  # 鱼桶中第一条鱼位置
MOUSE_SAFE_BIT_BASE = -80  # 鼠标移动安全位置 排除对鱼品质识别干扰
FISH_IS_LOCKED_REGION_BASE = (1924, 588, 25, 30, 'tr')  # 鱼上锁
FIRST_FISH_LOCATION = (1924, 640, 'tr')  # 第一条鱼坐标 1k(1444,480)
CLOSE_BUTTON_LOCATION = (2461, 445, 'tr')  # 关闭鱼桶坐标 1K(1844,333)
FISH_DISCARD_LOCATION = (1964, 800, 'tr')  # 丢弃鱼坐标 屏幕位置与FIRST_FISH_LOCATION保持一致
FISH_LOCKED_LOCATION = (1964, 860, 'tr')  # 锁定鱼坐标 屏幕位置与FIRST_FISH_LOCATION保持一致

FISH_INFO_REGION_BASE = (915, 75, 725, 150, 'tc')  # 鱼信息识别区域
UNO_SKIP_INFO_REGION_BASE = (2269, 1339, 44, 44, 'br')  # uno跳过按钮
UNO_CLICK_LOCATION = (2323, 1339, 'br')  # uno 点击位置


class Location:
    # 全局配置单例
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.bait_region_base = BAIT_REGION_BASE
        self.bait_corp_location = BAIT_CORP_LOCATION
        self.fish_star_region_base = FISH_STAR_REGION_BASE
        self.f_1_region_base = F_1_REGION_BASE
        self.f_2_region_base = F_2_REGION_BASE
        self.fishing_region_base = FISHING_REGION_BASE
        self.overtime_region_base = OVERTIME_REGION_BASE
        self.btn_no_jiashi_base = BTN_NO_JIASHI_BASE
        self.btn_yes_jiashi_base = BTN_YES_JIASHI_BASE
        self.open_fish_bucket_bit_base = OPEN_FISH_BUCKET_BIT_BASE
        self.bucket_opened_region_base = BUCKET_OPENED_REGION_BASE
        self.bucket_full_region_base = BUCKET_FULL_REGION_BASE
        self.no_bait_region_base = NO_BAIT_REGION_BASE
        self.bucket_left_num_region_base = BUCKET_LEFT_NUM_REGION_BASE
        self.bucket_empty_region_base = BUCKET_EMPTY_REGION_BASE
        self.fish_color_info_location = FISH_COLOR_INFO_LOCATION
        self.fish_is_locked_region_base = FISH_IS_LOCKED_REGION_BASE
        self.first_fish_location = FIRST_FISH_LOCATION
        self.close_button_location = CLOSE_BUTTON_LOCATION
        self.fish_discard_location = FISH_DISCARD_LOCATION
        self.fish_locked_location = FISH_LOCKED_LOCATION
        self.fish_info_region_base = FISH_INFO_REGION_BASE
        self.mouse_safe_bit_base = MOUSE_SAFE_BIT_BASE
        self.waiting_strike_region_base = WAITING_STRIKE_REGION_BASE
        self.drag_fish_region_base = DRAG_FISH_REGION_BASE
        self.uno_skip_info_region_base = UNO_SKIP_INFO_REGION_BASE
        self.uno_click_location = UNO_CLICK_LOCATION

    # 更新位置信息
    def update_location(self):
        self.bait_region_base = scale_corner_anchored(*BAIT_REGION_BASE)
        self.bait_corp_location = scale_point_anchored(*BAIT_CORP_LOCATION)
        self.fish_star_region_base = scale_corner_anchored(*FISH_STAR_REGION_BASE)
        self.f_1_region_base = scale_corner_anchored(*F_1_REGION_BASE)
        self.f_2_region_base = scale_corner_anchored(*F_2_REGION_BASE)
        self.fishing_region_base = scale_corner_anchored(*FISHING_REGION_BASE)
        self.overtime_region_base = scale_corner_anchored(*OVERTIME_REGION_BASE)
        self.btn_no_jiashi_base = scale_point_anchored(*BTN_NO_JIASHI_BASE)
        self.btn_yes_jiashi_base = scale_point_anchored(*BTN_YES_JIASHI_BASE)
        self.open_fish_bucket_bit_base = scale_cords_x(OPEN_FISH_BUCKET_BIT_BASE)
        self.bucket_opened_region_base = scale_corner_anchored(*BUCKET_OPENED_REGION_BASE)
        self.bucket_full_region_base = scale_corner_anchored(*BUCKET_FULL_REGION_BASE)
        self.no_bait_region_base = scale_corner_anchored(*NO_BAIT_REGION_BASE)
        self.bucket_left_num_region_base = scale_corner_anchored(*BUCKET_LEFT_NUM_REGION_BASE)
        self.bucket_empty_region_base = scale_corner_anchored(*BUCKET_EMPTY_REGION_BASE)
        self.fish_color_info_location = scale_point_anchored(*FISH_COLOR_INFO_LOCATION)
        self.fish_is_locked_region_base = scale_corner_anchored(*FISH_IS_LOCKED_REGION_BASE)
        self.first_fish_location = scale_point_anchored(*FIRST_FISH_LOCATION)
        self.close_button_location = scale_point_anchored(*CLOSE_BUTTON_LOCATION)
        self.fish_discard_location = scale_point_anchored(*FISH_DISCARD_LOCATION)
        self.fish_locked_location = scale_point_anchored(*FISH_LOCKED_LOCATION)
        self.fish_info_region_base = scale_corner_anchored(*FISH_INFO_REGION_BASE)
        self.mouse_safe_bit_base = scale_cords_x(MOUSE_SAFE_BIT_BASE)
        self.waiting_strike_region_base = scale_corner_anchored(*WAITING_STRIKE_REGION_BASE)
        self.drag_fish_region_base = scale_corner_anchored(*DRAG_FISH_REGION_BASE)
        self.uno_skip_info_region_base = scale_corner_anchored(*UNO_SKIP_INFO_REGION_BASE)
        self.uno_click_location = scale_point_anchored(*UNO_CLICK_LOCATION)

    # 重新加载
    def reload_base_date(self):
        self.bait_region_base = BAIT_REGION_BASE
        self.fish_star_region_base = FISH_STAR_REGION_BASE
        self.f_1_region_base = F_1_REGION_BASE
        self.f_2_region_base = F_2_REGION_BASE
        self.fishing_region_base = FISHING_REGION_BASE
        self.overtime_region_base = OVERTIME_REGION_BASE
        self.btn_no_jiashi_base = BTN_NO_JIASHI_BASE
        self.btn_yes_jiashi_base = BTN_YES_JIASHI_BASE
        self.open_fish_bucket_bit_base = OPEN_FISH_BUCKET_BIT_BASE
        self.bucket_opened_region_base = BUCKET_OPENED_REGION_BASE
        self.bucket_full_region_base = BUCKET_FULL_REGION_BASE
        self.no_bait_region_base = scale_corner_anchored(*NO_BAIT_REGION_BASE)
        self.bucket_left_num_region_base = BUCKET_LEFT_NUM_REGION_BASE
        self.bucket_empty_region_base = BUCKET_EMPTY_REGION_BASE
        self.fish_color_info_location = FISH_COLOR_INFO_LOCATION
        self.fish_is_locked_region_base = FISH_IS_LOCKED_REGION_BASE
        self.first_fish_location = FIRST_FISH_LOCATION
        self.close_button_location = CLOSE_BUTTON_LOCATION
        self.fish_discard_location = FISH_DISCARD_LOCATION
        self.fish_locked_location = FISH_LOCKED_LOCATION
        self.fish_info_region_base = FISH_INFO_REGION_BASE
        self.mouse_safe_bit_base = scale_cords_x(MOUSE_SAFE_BIT_BASE)
        self.waiting_strike_region_base = scale_corner_anchored(*WAITING_STRIKE_REGION_BASE)
        self.drag_fish_region_base = scale_corner_anchored(*DRAG_FISH_REGION_BASE)
        self.uno_skip_info_region_base = scale_corner_anchored(*UNO_SKIP_INFO_REGION_BASE)
        self.uno_click_location = scale_point_anchored(*UNO_CLICK_LOCATION)


location = Location()
