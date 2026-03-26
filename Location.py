from ScreenAdapt import screen_adaptation_rectangle, screen_adaptation_point, screen_adaptation_x

# 位置信息(基准"2k")
BAIT_REGION_BASE = (2318, 1296, 30, 22)  # 鱼饵数量区域
BAIT_TEN = (0, 22, 0, 15)  # 十位
BAIT_ONE = (0, 22, 15, 30)  # 个位
BAIT_MID = (0, 22, 7, 15)  # 中间位
FISH_STAR_REGION_BASE = (1172, 165, 34, 34)  # 上鱼星星
F_1_REGION_BASE = (1100, 1329, 10, 19)  # F1位置
F_2_REGION_BASE = (1212, 1329, 10, 19)  # F2位置
FISHING_REGION_BASE = (1146, 1316, 17, 21)  # 上鱼右键

OVERTIME_REGION_BASE = (1245, 675, 26, 27)  # 加时界面检测区域
BTN_NO_JIASHI_BASE = (1182, 776)  # 不加时按钮
BTN_YES_JIASHI_BASE = (1398, 776)  # 加时按钮

OPEN_FISH_BUCKET_BIT_BASE = -200  # 打开鱼桶鼠标移动
BUCKET_OPENED_REGION_BASE = (2145, 408, 34, 36)  # 桶以打开
BUCKET_FULL_REGION_BASE = (1184, 434, 36, 38)  # 鱼桶满了(满)
BUCKET_LEFT_NUM_REGION_BASE = (2148, 457, 21, 28)  # 鱼桶已装(48)
BUCKET_EMPTY_REGION_BASE = (2111, 909, 33, 34)  # 鱼桶一条鱼也没有(空)
FISH_COLOR_INFO_LOCATION = (1924, 640)  # 鱼桶中第一条鱼位置
FISH_IS_LOCKED_REGION_BASE = (1924, 588, 23, 29)  # 鱼上锁
FIRST_FISH_LOCATION = (1924, 640)  # 第一条鱼坐标
CLOSE_BUTTON_LOCATION = (2461, 445)  # 关闭鱼桶坐标
FISH_DISCARD_LOCATION = (1964, 800)  # 丢弃鱼坐标
FISH_LOCKED_LOCATION = (1964, 860)  # 锁定鱼坐标


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
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.off_x = 0
        self.off_y = 0
        self.bait_region_base = BAIT_REGION_BASE
        self.bait_ten = BAIT_TEN
        self.bait_one = BAIT_ONE
        self.bait_mid = BAIT_MID
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
        self.bucket_left_num_region_base = BUCKET_LEFT_NUM_REGION_BASE
        self.bucket_empty_region_base = BUCKET_EMPTY_REGION_BASE
        self.fish_color_info_location = FISH_COLOR_INFO_LOCATION
        self.fish_is_locked_region_base = FISH_IS_LOCKED_REGION_BASE
        self.first_fish_location = FIRST_FISH_LOCATION
        self.close_button_location = CLOSE_BUTTON_LOCATION
        self.fish_discard_location = FISH_DISCARD_LOCATION
        self.fish_locked_location = FISH_LOCKED_LOCATION

    def calculate_off(self):
        from GlobalConfig import global_config
        self.scale_x = global_config.scale_x
        self.scale_y = global_config.scale_y
        self.off_x = global_config.params['custom_width'] - global_config.params['base_width']
        self.off_y = global_config.params['base_height'] - global_config.params['base_height']

    # 更新位置信息(基于分辨率比例不变)
    def update_location_percentage_not_change(self):
        self.bait_region_base = screen_adaptation_rectangle(*BAIT_REGION_BASE)
        self.bait_ten = screen_adaptation_rectangle(*BAIT_TEN)
        self.bait_one = screen_adaptation_rectangle(*BAIT_ONE)
        self.bait_mid = screen_adaptation_rectangle(*BAIT_MID)
        self.fish_star_region_base = screen_adaptation_rectangle(*FISH_STAR_REGION_BASE)
        self.f_1_region_base = screen_adaptation_rectangle(*F_1_REGION_BASE)
        self.f_2_region_base = screen_adaptation_rectangle(*F_2_REGION_BASE)
        self.fishing_region_base = screen_adaptation_rectangle(*FISHING_REGION_BASE)
        self.overtime_region_base = screen_adaptation_rectangle(*OVERTIME_REGION_BASE)
        self.btn_no_jiashi_base = screen_adaptation_point(*BTN_NO_JIASHI_BASE)
        self.btn_yes_jiashi_base = screen_adaptation_point(*BTN_YES_JIASHI_BASE)
        self.open_fish_bucket_bit_base = screen_adaptation_x(OPEN_FISH_BUCKET_BIT_BASE)
        self.bucket_opened_region_base = screen_adaptation_rectangle(*BUCKET_OPENED_REGION_BASE)
        self.bucket_full_region_base = screen_adaptation_rectangle(*BUCKET_FULL_REGION_BASE)
        self.bucket_left_num_region_base = screen_adaptation_rectangle(*BUCKET_LEFT_NUM_REGION_BASE)
        self.bucket_empty_region_base = screen_adaptation_rectangle(*BUCKET_EMPTY_REGION_BASE)
        self.fish_color_info_location = screen_adaptation_point(*FISH_COLOR_INFO_LOCATION)
        self.fish_is_locked_region_base = screen_adaptation_rectangle(*FISH_IS_LOCKED_REGION_BASE)
        self.first_fish_location = screen_adaptation_point(*FIRST_FISH_LOCATION)
        self.close_button_location = screen_adaptation_point(*CLOSE_BUTTON_LOCATION)
        self.fish_discard_location = screen_adaptation_point(*FISH_DISCARD_LOCATION)
        self.fish_locked_location = screen_adaptation_point(*FISH_LOCKED_LOCATION)

    # 更新位置信息(基于分辨率比例不变)
    def update_location_percentage_change(self):
        self.bait_region_base = screen_adaptation_rectangle(*BAIT_REGION_BASE)
        self.bait_ten = screen_adaptation_rectangle(*BAIT_TEN)
        self.bait_one = screen_adaptation_rectangle(*BAIT_ONE)
        self.bait_mid = screen_adaptation_rectangle(*BAIT_MID)
        self.fish_star_region_base = screen_adaptation_rectangle(*FISH_STAR_REGION_BASE)
        self.f_1_region_base = screen_adaptation_rectangle(*F_1_REGION_BASE)
        self.f_2_region_base = screen_adaptation_rectangle(*F_2_REGION_BASE)
        self.fishing_region_base = screen_adaptation_rectangle(*FISHING_REGION_BASE)
        self.overtime_region_base = screen_adaptation_rectangle(*OVERTIME_REGION_BASE)
        self.btn_no_jiashi_base = screen_adaptation_point(*BTN_NO_JIASHI_BASE)
        self.btn_yes_jiashi_base = screen_adaptation_point(*BTN_YES_JIASHI_BASE)
        self.open_fish_bucket_bit_base = screen_adaptation_x(OPEN_FISH_BUCKET_BIT_BASE)
        self.bucket_opened_region_base = screen_adaptation_rectangle(*BUCKET_OPENED_REGION_BASE)
        self.bucket_full_region_base = screen_adaptation_rectangle(*BUCKET_FULL_REGION_BASE)
        self.bucket_left_num_region_base = screen_adaptation_rectangle(*BUCKET_LEFT_NUM_REGION_BASE)
        self.bucket_empty_region_base = screen_adaptation_rectangle(*BUCKET_EMPTY_REGION_BASE)
        self.fish_color_info_location = screen_adaptation_point(*FISH_COLOR_INFO_LOCATION)
        self.fish_is_locked_region_base = screen_adaptation_rectangle(*FISH_IS_LOCKED_REGION_BASE)
        self.first_fish_location = screen_adaptation_point(*FIRST_FISH_LOCATION)
        self.close_button_location = screen_adaptation_point(*CLOSE_BUTTON_LOCATION)
        self.fish_discard_location = screen_adaptation_point(*FISH_DISCARD_LOCATION)
        self.fish_locked_location = screen_adaptation_point(*FISH_LOCKED_LOCATION)


location = Location()
