import cv2
import numpy as np

from GlobalConfig import global_config


# 分辨率适配
def screen_adaptation_rectangle(x, y, w, h):
    return int(x * global_config.scale_x), int(y * global_config.scale_y), int(w * global_config.scale_x), int(
        h + global_config.scale_y)


# 分辨率适配
def screen_adaptation_point(x, y):
    return int(x * global_config.scale_x), int(y * global_config.scale_y)


# 分辨率适配
def screen_adaptation_x(x):
    return int(x * global_config.scale_x)


# 截取屏幕区域
def capture_region(x, y, w, h, tp):
    region = (x, y, x + w, y + h)
    frame = global_config.scr.grab(region)
    if frame is None:
        return None
    img_arr = np.array(frame)  # screenshot �?ScreenShot 类型，转换为 NumPy 数组
    img = cv2.cvtColor(img_arr, tp)
    return img

# 灰度截取
def capture_region_rgb(x, y, w, h):
    return capture_region(x, y, w, h, cv2.COLOR_BGRA2RGB)

# 灰度截取
def capture_region_gary(x, y, w, h):
    return capture_region(x, y, w, h, cv2.COLOR_RGBA2GRAY)
