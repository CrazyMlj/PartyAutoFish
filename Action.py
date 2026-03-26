import ctypes
import os

import cv2
import mss
import numpy as np
from PIL import Image

from GlobalConfig import global_config
from MouseOrKeyBoardUtil import hold_mouse_left_button, key_press, POINT, key_release, \
    hold_mouse_right_button, _default_mouse
from ScreenAdapt import screen_adaptation, capture_region_gary, screen_adaptation_3, screen_adaptation_2, \
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

# 数字模板
bait_ten = 0
bait_one = 0

# 图片模板
num_templates = None
star_template = None
f1_template = None
f2_template = None
fishing_template = None
bucket_opened_template = None
lock_template = None
over_time_template = None
bucket_full_template = None
bucket_empty_template = None


# ========================
# 模板加载
# ========================
def load_templates():
    load_num_templates()
    load_star_template()
    load_f1_template()
    load_f2_template()
    load_fishing_template()
    load_over_time_template()
    load_bucket_opened_template()
    load_lock_template()
    load_bucket_full_template()
    load_bucket_empty_template()


# 加载模板（0.png到9.png）
def load_num_templates():
    global num_templates, template_folder_path
    if num_templates is None:
        num_templates = []
        for i in range(10):
            template_path = os.path.join(template_folder_path, f"{i}_grayscale.png")
            img = Image.open(template_path)
            template = np.array(img)
            num_templates.append(template)
    return num_templates


# 加载模板
def load(template: str):
    global template_folder_path
    if template is not None:
        template_path = os.path.join(template_folder_path, template)
        img = Image.open(template_path)
        template_img_arr = np.array(img)
        return template_img_arr
    return None


def load_star_template():
    global star_template
    star_template = load("star_grayscale.png")
    return star_template


def load_f1_template():
    global f1_template
    f1_template = load("F1_grayscale.png")
    return f1_template


def load_f2_template():
    global f2_template
    f2_template = load("F2_grayscale.png")
    return f2_template


def load_fishing_template():
    global fishing_template
    fishing_template = load("shangyu_grayscale.png")
    return fishing_template


def load_over_time_template():
    global over_time_template
    over_time_template = load("chang_grayscale.png")
    return over_time_template


def load_bucket_opened_template():
    global bucket_opened_template
    bucket_opened_template = load("bucket_opened_grayscale.png")
    return bucket_opened_template


def load_lock_template():
    global lock_template
    lock_template = load("lock_grayscale.png")
    return lock_template


def load_bucket_full_template():
    global bucket_full_template
    bucket_full_template = load("bucket_full_grayscale.png")
    return bucket_full_template


def load_bucket_empty_template():
    global bucket_empty_template
    bucket_empty_template = load("bucket_empty_grayscale.png")
    return bucket_empty_template


# ========================
# 识别数字
# ========================
def bait_math_val():
    global bait_ten, bait_one
    # 使用缩放后的坐标
    region_base = screen_adaptation(*BAIT_REGION_BASE)
    gray_img = capture_region_gary(*region_base)
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
    global num_templates
    best_match = None  # 最佳匹配信息
    best_val = 0  # 存储最佳匹配度
    for i, template in enumerate(num_templates):
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8 and max_val > best_val:  # 找到最佳匹配
            best_val = max_val
            best_match = (i, max_loc)  # 记录最佳匹配的数字和位置
    return best_match


# ========================
# 识别c
# ========================
# 基本识别方法
def match(region_base, template):
    region_base = screen_adaptation(*region_base)
    # 获取区域坐标并捕获灰度图
    region_gray = capture_region_gary(*region_base)
    if region_gray is None:
        return None
    # 执行模板匹配并检查最大匹配度是否大于 0.8
    return cv2.minMaxLoc(cv2.matchTemplate(region_gray, template, cv2.TM_CCOEFF_NORMED))[1] > 0.8


def fished_match():
    global FISH_STAR_REGION_BASE, star_template
    return match(FISH_STAR_REGION_BASE, star_template)


def f1_matched():
    global F_1_REGION_BASE, f1_template
    return match(F_1_REGION_BASE, f1_template)


def f2_matched():
    global F_2_REGION_BASE, f2_template
    return match(F_2_REGION_BASE, f2_template)


def fishing_matched():
    global FISHING_REGION_BASE, fishing_template
    return match(FISHING_REGION_BASE, fishing_template)


def overtime_matched():
    global OVERTIME_REGION_BASE, over_time_template
    return match(OVERTIME_REGION_BASE, over_time_template)


# 桶是否已打开
def bucket_opened_matched():
    global BUCKET_OPENED_REGION_BASE, bucket_opened_template
    return match(BUCKET_OPENED_REGION_BASE, bucket_opened_template)


# 鱼是否已经锁住
def locked_fish_matched():
    global FISH_IS_LOCKED_REGION_BASE, lock_template
    return match(FISH_IS_LOCKED_REGION_BASE, lock_template)


# 桶是否已满(提示词"鱼桶已满")
def bucket_full_matched():
    global BUCKET_FULL_REGION_BASE, bucket_full_template
    return match(BUCKET_FULL_REGION_BASE, bucket_full_template)


# 桶是否为空
def bucket_empty_matched():
    global BUCKET_EMPTY_REGION_BASE, bucket_empty_template
    return match(BUCKET_EMPTY_REGION_BASE, bucket_empty_template)


# 桶是否有48条鱼
def bucket_48_matched():
    global BUCKET_LEFT_NUM_REGION_BASE
    BUCKET_LEFT_NUM_REGION_BASE = screen_adaptation(*BUCKET_LEFT_NUM_REGION_BASE)
    match_frame = global_config.scr.grab(BUCKET_LEFT_NUM_REGION_BASE)
    if match_frame is not None:
        img = np.array(match_frame)
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        region1 = gray_img[0:28, 0:21]  # 获取区域1的图像
        region2 = gray_img[9:37, 0:21]  # 获取区域2的图像
        return cv2.minMaxLoc(cv2.matchTemplate(region1, region2, cv2.TM_CCOEFF_NORMED))[1] > 0.95
    return False


# 识别鱼品质
def recognize_fish_quality(tolerance):
    global FISH_COLOR_INFO_REGION_BASE
    img = capture_region_rgb(*FISH_COLOR_INFO_REGION_BASE)
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
    global BTN_YES_JIASHI_BASE
    x, y = screen_adaptation_2(*BTN_YES_JIASHI_BASE)
    mouse.move(x, y)
    hold_mouse_left_button(0.1)


# 不加时
def overtime_n():
    global BTN_NO_JIASHI_BASE
    x, y = screen_adaptation_2(*BTN_NO_JIASHI_BASE)
    mouse.move(x, y)
    hold_mouse_left_button(0.1)


# 打开鱼桶界面
def open_fish_bucket():
    global OPEN_FISH_BUCKET_BIT_BASE
    # 长按按c键打开 移动鼠标到鱼桶图标 释放c键打开鱼桶
    key_press(67, 1, True)
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    mouse.move(point.x + screen_adaptation_3(OPEN_FISH_BUCKET_BIT_BASE), point.y)
    key_release(67)


# 关闭鱼桶界面
def close_fish_bucket():
    global CLOSE_BUTTON_LOCATION
    x, y = screen_adaptation_2(*CLOSE_BUTTON_LOCATION)
    # 移动鼠标至关闭图标按钮
    mouse.move(x, y)
    hold_mouse_left_button(0.1)


# 锁定鱼
def lock_fish():
    global FIRST_FISH_LOCATION, FISH_LOCKED_LOCATION
    x, y = screen_adaptation_2(*FIRST_FISH_LOCATION)
    x1, y1 = screen_adaptation_2(*FISH_LOCKED_LOCATION)
    # 移动鼠标到第一条鱼上 单击鼠标右键 移动鼠标至"锁定" 单击鼠标左键
    mouse.move(x, y)
    hold_mouse_right_button(0.1)
    mouse.move(x1, y1)
    hold_mouse_left_button(0.1)
    # 鼠标复位
    mouse.move(x, y)


# 放生鱼
def discard_fish():
    global FIRST_FISH_LOCATION, FISH_DISCARD_LOCATION
    x, y = screen_adaptation_2(*FIRST_FISH_LOCATION)
    x1, y1 = screen_adaptation_2(*FISH_DISCARD_LOCATION)
    # 移动鼠标到第一条鱼上 单击鼠标右键 移动鼠标至"放生" 单击鼠标左键
    mouse.move(x, y)
    hold_mouse_right_button(0.1)
    mouse.move(x1, y1)
    hold_mouse_left_button(0.1)
    # 鼠标复位
    mouse.move(x, y)
