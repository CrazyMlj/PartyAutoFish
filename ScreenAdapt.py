import cv2
import numpy as np

from GlobalConfig import global_config


# 分辨率适配
def screen_adaptation(x, y, w, h):
    return int(x * global_config.scale_x), int(y * global_config.scale_y), int(w * global_config.scale_x), int(
        h + global_config.scale_y)


# 分辨率适配
def screen_adaptation_2(x, y):
    return int(x * global_config.scale_x), int(y * global_config.scale_y)


# 分辨率适配
def screen_adaptation_3(x):
    return int(x * global_config.scale_x)


# 截取屏幕区域
def capture_region(x, y, w, h, tp):
    region = (x, y, x + w, y + h)
    frame = global_config.scr.grab(region)
    if frame is None:
        return None
    img_arr = np.array(frame)  # screenshot �?ScreenShot 类型，转换为 NumPy 数组
    img = cv2.cvtColor(img_arr, tp)  # cv2.COLOR_BGRA2RGB
    return img


# 灰度截取
def capture_region_gary(x, y, w, h):
    return capture_region(x, y, w, h, cv2.COLOR_RGBA2GRAY)
