import ctypes
import os

import cv2
import mss
import numpy as np
from PIL import Image

from GlobalConfig import global_config
from MouseOrKeyBoardUtil import hold_mouse_left_button, key_press, POINT, key_release, \
    hold_mouse_right_button, _default_mouse
from ScreenAdapt import screen_adaptation_rectangle, capture_region_gary, screen_adaptation_x, screen_adaptation_point, \
    capture_region, capture_region_rgb

template_folder_path = os.path.join('.', 'resources')
user32 = ctypes.WinDLL("user32")
mouse = _default_mouse
scr = mss.mss()

# 位置信息(基准"2k")
BAIT_REGION_BASE = (2318, 1296, 30, 22)  # 鱼饵数量区域
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
BUCKET_LEFT_NUM_REGION_BASE = (2148, 457, 2215, 478)  # 鱼桶已装(48)
BUCKET_EMPTY_REGION_BASE = (2111, 909, 33, 34)  # 鱼桶一条鱼也没有(空)
FISH_COLOR_INFO_REGION_BASE = (1924, 640, 1, 1)  # 鱼桶中第一条鱼位置
FISH_IS_LOCKED_REGION_BASE = (1924, 588, 23, 29)  # 鱼上锁
FIRST_FISH_LOCATION = (1924, 640)  # 第一条鱼坐标
CLOSE_BUTTON_LOCATION = (2461, 445)  # 关闭鱼桶坐标
FISH_DISCARD_LOCATION = (1964, 800)  # 丢弃鱼坐标
FISH_LOCKED_LOCATION = (1964, 860)  # 锁定鱼坐标

QUALITY_COLORS = {
    1: [181, 185, 190],  # 标准
    2: [140, 196, 85],  # 非凡
    3: [110, 172, 241],  # 稀有
    4: [169, 102, 249],  # 史诗
    5: [250, 198, 59]  # 传奇
}


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
        self.fish_color_info_region_base = FISH_COLOR_INFO_REGION_BASE
        self.fish_is_locked_region_base = FISH_IS_LOCKED_REGION_BASE
        self.first_fish_location = FIRST_FISH_LOCATION
        self.close_button_location = CLOSE_BUTTON_LOCATION
        self.fish_discard_location = FISH_DISCARD_LOCATION
        self.fish_locked_location = FISH_LOCKED_LOCATION

    #todo 更新位置信息(基于分辨率变化)

location = Location()


def load(template: str):
    global template_folder_path
    if template is not None:
        template_path = os.path.join(template_folder_path, template)
        img = Image.open(template_path)
        template_img_arr = np.array(img)
        return template_img_arr
    return None


class Template:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.num_templates = None
        self.star_template = None
        self.f1_template = None
        self.f2_template = None
        self.fishing_template = None
        self.bucket_opened_template = None
        self.lock_template = None
        self.over_time_template = None
        self.bucket_full_template = None
        self.bucket_empty_template = None

    # 模板加载
    def load_templates(self):
        self.load_num_templates()
        self.load_star_template()
        self.load_f1_template()
        self.load_f2_template()
        self.load_fishing_template()
        self.load_over_time_template()
        self.load_bucket_opened_template()
        self.load_lock_template()
        self.load_bucket_full_template()
        self.load_bucket_empty_template()

    def load_star_template(self):
        self.star_template = load("star_grayscale.png")
        return self.star_template

    def load_f1_template(self):
        self.f1_template = load("F1_grayscale.png")
        return self.f1_template

    def load_f2_template(self):
        self.f2_template = load("F2_grayscale.png")
        return self.f2_template

    def load_fishing_template(self):
        self.fishing_template = load("shangyu_grayscale.png")
        return self.fishing_template

    def load_over_time_template(self):
        self.over_time_template = load("chang_grayscale.png")
        return self.over_time_template

    def load_bucket_opened_template(self):
        self.bucket_opened_template = load("bucket_opened_grayscale.png")
        return self.bucket_opened_template

    def load_lock_template(self):
        self.lock_template = load("lock_grayscale.png")
        return self.lock_template

    def load_bucket_full_template(self):
        self.bucket_full_template = load("bucket_full_grayscale.png")
        return self.bucket_full_template

    def load_bucket_empty_template(self):
        self.bucket_empty_template = load("bucket_empty_grayscale.png")
        return self.bucket_empty_template

    # 加载模板（0.png到9.png）
    def load_num_templates(self):
        global template_folder_path
        if self.num_templates is None:
            self.num_templates = []
            for i in range(10):
                template_path = os.path.join(template_folder_path, f"{i}_grayscale.png")
                img = Image.open(template_path)
                template = np.array(img)
                self.num_templates.append(template)
        return self.num_templates

png_template = Template()


# ========================
# 识别数字
# ========================
def bait_math_val():
    gray_img = capture_region_gary(*location.bait_region_base)
    # 截取并处理区域1
    bait_ten = gray_img[0:22, 0:15]  # 获取区域1的图像 15 * 22
    best_match1 = match_digit_template(bait_ten)
    # 截取并处理区域2
    bait_one = gray_img[0:22, 15:30]  # 获取区域2的图像 15 * 22
    best_match2 = match_digit_template(bait_one)
    region3 = gray_img[0:22, 7:22]  # 获取区域3的图像 15 * 22
    best_match3 = match_digit_template(region3)
    if best_match1 and best_match2:
        # 从best_match中提取数字索引（i），并拼接成整数
        best_match1_val = best_match1[0]  # 提取区域1的数字索引
        best_match2_val = best_match2[0]  # 提取区域2的数字索引
        # 拼接两个匹配的数字，转换为整数
        global_config.bait_count_val = int(f"{best_match1_val}{best_match2_val}")
    elif best_match3:
        global_config.bait_count_val = int(f'{best_match3[0]}')
    else:
        global_config.bait_count_val = None
    return global_config.bait_count_val


def match_digit_template(image):
    best_match = None  # 最佳匹配信息
    best_val = 0  # 存储最佳匹配度
    for i, template in enumerate(png_template.num_templates):
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8 and max_val > best_val:  # 找到最佳匹配
            best_val = max_val
            best_match = (i, max_loc)  # 记录最佳匹配的数字和位置
    return best_match


# ========================
# 识别
# ========================
# 基本识别方法
def match(region_base, template):
    # 获取区域坐标并捕获灰度图
    region_gray = capture_region_gary(*region_base)
    if region_gray is None:
        return None
    # 执行模板匹配并检查最大匹配度是否大于 0.8
    return cv2.minMaxLoc(cv2.matchTemplate(region_gray, template, cv2.TM_CCOEFF_NORMED))[1] > 0.8


def fished_match():
    return match(location.fish_star_region_base, png_template.star_template)


def f1_matched():
    return match(location.f_1_region_base, png_template.f1_template)


def f2_matched():
    return match(location.f_2_region_base, png_template.f2_template)


def fishing_matched():
    return match(location.fishing_region_base, png_template.fishing_template)


def overtime_matched():
    return match(location.overtime_region_base, png_template.over_time_template)


# 桶是否已打开
def bucket_opened_matched():
    return match(location.bucket_opened_region_base, png_template.bucket_opened_template)


# 鱼是否已经锁住
def locked_fish_matched():
    return match(location.fish_is_locked_region_base, png_template.lock_template)


# 桶是否已满(提示词"鱼桶已满")
def bucket_full_matched():
    return match(location.bucket_full_region_base, png_template.bucket_full_template)


# 桶是否为空
def bucket_empty_matched():
    return match(location.bucket_empty_region_base, png_template.bucket_empty_template)


# 桶是否有48条鱼
def bucket_48_matched():
    global BUCKET_LEFT_NUM_REGION_BASE
    BUCKET_LEFT_NUM_REGION_BASE = screen_adaptation_rectangle(*BUCKET_LEFT_NUM_REGION_BASE)
    match_frame = global_config.scr.grab(location.bucket_left_num_region_base)
    if match_frame is not None:
        img = np.array(match_frame)
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        region1 = gray_img[0:28, 0:21]  # 获取区域1的图像
        region2 = gray_img[9:37, 0:21]  # 获取区域2的图像
        return cv2.minMaxLoc(cv2.matchTemplate(region1, region2, cv2.TM_CCOEFF_NORMED))[1] > 0.95
    return False


# 识别鱼品质
def recognize_fish_quality(tolerance):
    img = capture_region_rgb(*location.fish_color_info_region_base)
    for QUALITY_COLOR in QUALITY_COLORS.items():
        distance = sum((img[0][0][i] - QUALITY_COLOR[1][i]) for i in range(3))
        if distance <= tolerance:
            return QUALITY_COLOR[0]
    return None


# ========================
# 操作
# ========================
# 加时
def overtime_y():
    mouse.move(*location.btn_yes_jiashi_base)
    hold_mouse_left_button(0.1)


# 不加时
def overtime_n():
    mouse.move(*location.btn_no_jiashi_base)
    hold_mouse_left_button(0.1)


# 打开鱼桶界面
def open_fish_bucket():
    # 长按按c键打开 移动鼠标到鱼桶图标 释放c键打开鱼桶
    key_press(67, 1, True)
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    mouse.move(point.x + screen_adaptation_x(location.open_fish_bucket_bit_base), point.y)
    key_release(67)


# 关闭鱼桶界面
def close_fish_bucket():
    # 移动鼠标至关闭图标按钮
    mouse.move(*location.close_button_location)
    hold_mouse_left_button(0.1)


# 锁定鱼
def lock_fish():
    # 移动鼠标到第一条鱼上 单击鼠标右键 移动鼠标至"锁定" 单击鼠标左键
    mouse.move(*location.first_fish_location)
    hold_mouse_right_button(0.1)
    mouse.move(*location.fish_locked_location)
    hold_mouse_left_button(0.1)
    # 鼠标复位
    mouse.move(*location.first_fish_location)


# 放生鱼
def discard_fish():
    # 移动鼠标到第一条鱼上 单击鼠标右键 移动鼠标至"放生" 单击鼠标左键
    mouse.move(*location.first_fish_location)
    hold_mouse_right_button(0.1)
    mouse.move(*location.fish_discard_location)
    hold_mouse_left_button(0.1)
    # 鼠标复位
    mouse.move(*location.first_fish_location)
