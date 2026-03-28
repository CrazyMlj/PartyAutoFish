import ctypes
import math
import random
import threading
import time

from GlobalConfig import global_config

JITTER_RANGE_PERCENTAGE = 40

user32 = ctypes.WinDLL("user32")
mouse_lock = threading.Lock()
is_mouse_left_down = False
is_mouse_right_down = False


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def ease_in_out_cubic(t):
    # 缓动函数
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2


class HumanLikeMouse:
    def __init__(self):
        self.base_speed = 10  # 基础移动速度
        self.jitter = 2  # 抖动幅度

    # 模拟人类鼠标移动，包含速度变化和抖动
    def move(self, dest_x, dest_y):
        ensure_mouse_left_up()
        ensure_mouse_right_up()
        # 获取当前位置
        point = POINT()
        user32.GetCursorPos(ctypes.byref(point))
        curr_x, curr_y = point.x, point.y

        # 计算距离
        distance = math.hypot(dest_x - curr_x, dest_y - curr_y)

        # 计算总步数
        steps = max(10, int(distance / self.base_speed))

        # 速度曲线：慢->快->慢
        for i in range(steps + 1):
            t = i / steps  # 0 到 1

            # 速度曲线（正态分布形状）
            if t < 0.2:
                # 起始阶段：慢速
                speed_factor = 0.3 + t * 3.5
            elif t > 0.8:
                # 结束阶段：慢速
                speed_factor = 4 - (t - 0.8) * 15
            else:
                # 中间阶段：快速
                speed_factor = 1.0 + math.sin((t - 0.2) * math.pi / 0.6) * 0.5

            # 计算当前应该到达的位置
            current_t = ease_in_out_cubic(t)
            target_x = curr_x + (dest_x - curr_x) * current_t
            target_y = curr_y + (dest_y - curr_y) * current_t

            # 添加随机抖动（抖动随速度变化）
            jitter_amount = self.jitter * (1 - abs(speed_factor - 1)) * random.uniform(0.5, 1.5)
            final_x = target_x + random.uniform(-jitter_amount, jitter_amount)
            final_y = target_y + random.uniform(-jitter_amount, jitter_amount)

            # 移动鼠标
            user32.SetCursorPos(int(final_x), int(final_y))

            # 动态延迟
            delay = 0.005 / speed_factor * random.uniform(0.8, 1.2)
            time.sleep(delay)

        # 最终精确定位
        user32.SetCursorPos(dest_x, dest_y)

        # 偶尔添加过冲和回调（模拟人类）
        if random.random() < 0.3 and distance > 200:
            # 过冲5-10像素
            overshoot_x = dest_x + random.uniform(-10, 10)
            overshoot_y = dest_y + random.uniform(-10, 10)
            user32.SetCursorPos(int(overshoot_x), int(overshoot_y))
            time.sleep(random.uniform(0.02, 0.05))
            user32.SetCursorPos(dest_x, dest_y)

    def set_speed(self, speed_factor=0.5):
        # 调整整体速度
        self.base_speed = int(10 * speed_factor)
        self.jitter = 2 / speed_factor


# 加上抖动随机数
def add_jitter(base_time: float):
    global JITTER_RANGE_PERCENTAGE
    jitter_factor = random.uniform(1 - JITTER_RANGE_PERCENTAGE / 100, 1 + JITTER_RANGE_PERCENTAGE / 100)
    jittered_time = base_time * jitter_factor
    return max(0.01, round(jittered_time, 3))


def ensure_mouse_left_down():
    global is_mouse_left_down
    with mouse_lock:
        if not is_mouse_left_down:
            user32.mouse_event(0x02, 0, 0, 0, 0)  # 左键按下
            is_mouse_left_down = True


def ensure_mouse_left_up():
    global is_mouse_left_down
    with mouse_lock:
        if is_mouse_left_down:
            user32.mouse_event(0x04, 0, 0, 0, 0)  # 左键释放
            is_mouse_left_down = False


def ensure_mouse_right_down():
    global is_mouse_right_down
    with mouse_lock:
        if not is_mouse_right_down:
            user32.mouse_event(0x08, 0, 0, 0, 0)  # 右键按下
            is_mouse_right_down = True


def ensure_mouse_right_up():
    global is_mouse_right_down
    with mouse_lock:
        if is_mouse_right_down:
            user32.mouse_event(0x10, 0, 0, 0, 0)  # 右键释放
            is_mouse_right_down = False


def press_and_release_mouse_button():
    user32.mouse_event(0x02, 0, 0, 0, 0)
    time.sleep(add_jitter(global_config.params['mouse_left_hold_time']))
    user32.mouse_event(0x04, 0, 0, 0, 0)
    time.sleep(add_jitter(global_config.params['mouse_left_release_time']))


def hold_mouse_left_button(duration):
    global is_mouse_left_down
    if is_mouse_left_down:
        ensure_mouse_left_up()
    with mouse_lock:
        user32.mouse_event(0x02, 0, 0, 0, 0)
        time.sleep(add_jitter(duration))
        user32.mouse_event(0x04, 0, 0, 0, 0)


def hold_mouse_right_button(duration):
    global is_mouse_right_down
    if is_mouse_right_down:
        user32.mouse_event(0x08, 0, 0, 0, 0)
    with mouse_lock:
        user32.mouse_event(0x08, 0, 0, 0, 0)
        time.sleep(add_jitter(duration))
        user32.mouse_event(0x10, 0, 0, 0, 0)


def key_press(vk_code, duration, is_hold=False):
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(add_jitter(duration))
    if not is_hold:
        user32.keybd_event(vk_code, 0, 0x0002, 0)


def key_release(vk_code):
    user32.keybd_event(vk_code, 0, 0x0002, 0)


# 创建全局实例
_default_mouse = HumanLikeMouse()
