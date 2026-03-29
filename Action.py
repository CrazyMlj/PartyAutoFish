import ctypes
import math
import os

import cv2
import mss
import numpy as np
from PIL import Image

from GlobalConfig import global_config
from Location import location
from MouseOrKeyBoardUtil import hold_mouse_left_button, key_press, POINT, key_release, \
    hold_mouse_right_button, _default_mouse, ensure_mouse_left_up
from ScreenAdapt import scale_template

template_folder_path = os.path.join('.', 'resources')
user32 = ctypes.WinDLL("user32")
mouse = _default_mouse
scr = mss.mss()

QUALITY_COLORS = {
    1: [182, 186, 191],  # 标准
    2: [140, 196, 85],  # 非凡
    3: [110, 172, 241],  # 稀有
    4: [169, 102, 249],  # 史诗
    5: [250, 198, 59]  # 传奇 250 196 58
}


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
        self.bucket_48_template = None
        self.waiting_strike_or_drag_fish_template = None

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
        self.load_bucket_48_template()
        self.load_waiting_strike_or_drag_fish_template()

    def load_star_template(self):
        self.star_template = scale_template(load("star_grayscale.png"))
        return self.star_template

    def load_f1_template(self):
        self.f1_template = scale_template(load("F1_grayscale.png"))
        return self.f1_template

    def load_f2_template(self):
        self.f2_template = scale_template(load("F2_grayscale.png"))
        return self.f2_template

    def load_fishing_template(self):
        self.fishing_template = scale_template(load("shangyu_grayscale.png"))
        return self.fishing_template

    def load_over_time_template(self):
        self.over_time_template = scale_template(load("chang_grayscale.png"))
        return self.over_time_template

    def load_bucket_opened_template(self):
        self.bucket_opened_template = scale_template(load("bucket_opened_grayscale.png"))
        return self.bucket_opened_template

    def load_lock_template(self):
        self.lock_template = scale_template(load("lock_grayscale.png"))
        return self.lock_template

    def load_bucket_full_template(self):
        self.bucket_full_template = scale_template(load("bucket_full_grayscale.png"))
        return self.bucket_full_template

    def load_bucket_empty_template(self):
        self.bucket_empty_template = scale_template(load("bucket_empty_grayscale.png"))
        return self.bucket_empty_template

    def load_bucket_48_template(self):
        self.bucket_48_template = scale_template(load("bucket_48_grayscale.png"))

    def load_waiting_strike_or_drag_fish_template(self):
        self.waiting_strike_or_drag_fish_template = scale_template(load("waiting_strike_or_drag_fish_grayscale.png"))

    # 加载模板（0.png到9.png）
    def load_num_templates(self):
        global template_folder_path
        if self.num_templates is None:
            self.num_templates = []
            for i in range(10):
                template_path = os.path.join(template_folder_path, f"{i}_grayscale.png")
                img = Image.open(template_path)
                template = np.array(img)
                self.num_templates.append(scale_template(template))
        return self.num_templates


png_template = Template()


# ========================
# 识别数字
# ========================
def bait_match_val():
    gray_img = capture_region_gary(location.bait_region_base[0], location.bait_region_base[1],
                                   location.bait_region_base[2], location.bait_region_base[3])

    # 初始化匹配结果
    best_match1 = None
    best_match2 = None

    # 确保不超出图像边界
    img_h, img_w = gray_img.shape[:2]
    crop_h = min(location.bait_corp_location[1], img_h)
    crop_w = min(location.bait_corp_location[0], img_w // 2)  # 确保单个数字宽度不超过一半

    if crop_w <= img_w:
        # 截取并处理区域1
        bait_ten = gray_img[0:crop_h, 0:crop_w]  # 获取区域1的图像 15 * 22
        best_match1 = match_digit_template(bait_ten)

    if crop_w * 2 <= img_w:
        # 截取并处理区域2
        bait_one = gray_img[0:crop_h, crop_w:crop_w * 2]  # 获取区域2的图像 15 * 22
        best_match2 = match_digit_template(bait_one)

    mid_start = max(0, (img_w - crop_w) // 2)
    mid_end = min(mid_start + crop_w, img_w)
    region3 = gray_img[0:crop_h, mid_start:mid_end]  # 获取区域3的图像 15 * 22
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
    x, y, w, h = region_base[0], region_base[1], region_base[2], region_base[3]
    region_gray = capture_region_gary(x, y, w, h)
    if region_gray is None:
        return None
    # 执行模板匹配并检查最大匹配度是否大于 0.8
    min_max_loc = cv2.minMaxLoc(cv2.matchTemplate(region_gray, template, cv2.TM_CCOEFF_NORMED))[1]
    return min_max_loc > 0.8


def fished_matched():
    return match(location.fish_star_region_base, png_template.star_template)


def f1_matched():
    return match(location.f_1_region_base, png_template.f1_template)


def f2_matched():
    return match(location.f_2_region_base, png_template.f2_template)


def fishing_matched():
    return match(location.fishing_region_base, png_template.fishing_template)


def waiting_strike_matched():
    return match(location.waiting_strike_region_base, png_template.waiting_strike_or_drag_fish_template)


def drag_fish_matched():
    return match(location.drag_fish_region_base, png_template.waiting_strike_or_drag_fish_template)


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
    print(location.bucket_left_num_region_base)
    return match(location.bucket_left_num_region_base, png_template.bucket_48_template)


def is_color_similar_rgb(color1, color2, threshold=3):
    """
    判断两个RGB颜色是否相似
    color1, color2: (R, G, B) 元组或列表
    threshold: 阈值，越小越严格，推荐范围 20-50
    """
    # 计算欧几里得距离
    distance = math.sqrt((color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2)
    print(distance)
    return distance < threshold


# 识别鱼品质
def recognize_fish_quality():
    img = capture_region_rgb(location.fish_color_info_location[0], location.fish_color_info_location[1], 1, 1)
    img_arr = np.array(img)
    for QUALITY_COLOR in QUALITY_COLORS.items():
        if is_color_similar_rgb(img_arr[0, 0, :3], QUALITY_COLOR[1]):
            return QUALITY_COLOR[0]
    return None


# 截取鱼信息区域的图像
def capture_fish_info_region():
    return capture_region_rgb(location.fish_info_region_base[0], location.fish_info_region_base[1],
                              location.fish_info_region_base[2], location.fish_info_region_base[3])


# 截取屏幕区域
def capture_region(x, y, w, h, tp):
    region = (x, y, x + w, y + h)
    try:
        frame = global_config.get_scr().grab(region)
        if frame is None:
            return None
        img_arr = np.array(frame)
        img = cv2.cvtColor(img_arr, tp)
        return img
    except Exception as e:
        print(f"❌ [错误] 截取屏幕失败: {e}")
        return None


# 灰度截取
def capture_region_rgb(x, y, w, h):
    return capture_region(x, y, w, h, cv2.COLOR_BGRA2RGB)


# 灰度截取
def capture_region_gary(x, y, w, h):
    return capture_region(x, y, w, h, cv2.COLOR_RGBA2GRAY)


# ========================
# 操作
# ========================
# 加时
def overtime_y():
    ensure_mouse_left_up()
    mouse.move(location.btn_yes_jiashi_base[0], location.btn_yes_jiashi_base[1])
    hold_mouse_left_button(0.1)


# 不加时
def overtime_n():
    ensure_mouse_left_up()
    mouse.move(location.btn_no_jiashi_base[0], location.btn_no_jiashi_base[1])
    hold_mouse_left_button(0.1)


# 打开鱼桶界面
def open_fish_bucket():
    # 长按按c键打开 移动鼠标到鱼桶图标 释放c键打开鱼桶
    key_press(0x43, 1, True)
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    mouse.move(point.x + location.open_fish_bucket_bit_base, point.y)
    key_release(0x43)


# 收杆
def retrieve_the_rod():
    # 单击f
    key_press(0x46, 0.2, False)


# 关闭鱼桶界面
def close_fish_bucket():
    # 移动鼠标至关闭图标按钮
    mouse.move(location.close_button_location[0], location.close_button_location[1])
    hold_mouse_left_button(0.1)


# 锁定鱼
def lock_fish():
    # 移动鼠标到第一条鱼上 单击鼠标右键 移动鼠标至"锁定" 单击鼠标左键
    mouse.move(location.first_fish_location[0], location.first_fish_location[1])
    hold_mouse_right_button(0.1)
    mouse.move(location.fish_locked_location[0], location.fish_locked_location[1])
    hold_mouse_left_button(0.1)
    # 鼠标复位
    mouse.move(location.first_fish_location[0], location.first_fish_location[1])


# 放生鱼
def discard_fish():
    # 移动鼠标到第一条鱼上 单击鼠标右键 移动鼠标至"放生" 单击鼠标左键
    mouse.move(location.first_fish_location[0], location.first_fish_location[1])
    hold_mouse_right_button(0.1)
    mouse.move(location.fish_discard_location[0], location.fish_discard_location[1])
    hold_mouse_left_button(0.1)
    # 鼠标复位
    mouse.move(location.first_fish_location[0], location.first_fish_location[1])


# 移动鼠标到安全位置
def mouse_move_safe():
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    mouse.move(point.x + location.mouse_safe_bit_base, point.y)
