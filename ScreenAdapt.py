import cv2

from AnchorType import AnchorType
from GlobalConfig import global_config


# 根据分辨率缩放坐标（保持比例）
def scale_cords_by_percentage(x, y, w, h):
    return int(x * global_config.scale_uniform), int(y * global_config.scale_uniform), int(
        w * global_config.scale_uniform), int(h * global_config.scale_uniform)


def scale_cords_x(x):
    return int(x * global_config.scale_x)


# 缩放坐标 todo 优化 合并点与矩形
def scale_point_anchored(x, y, screen_location):
    new_x, new_y = x, y
    if global_config.scale_x == global_config.scale_y:
        new_x = x * global_config.scale_uniform
        new_y = y * global_config.scale_uniform
        return int(new_x), int(new_y), screen_location

    if AnchorType.from_string(screen_location) == AnchorType.CENTER:
        # 计算相对偏移
        offset_x = x - global_config.params['base_width'] / 2
        offset_y = y - global_config.params['base_height'] / 2

        # 缩放偏移
        new_offset_x = offset_x * global_config.scale_uniform
        new_offset_y = offset_y * global_config.scale_uniform
        new_x = global_config.params['custom_width'] / 2 + new_offset_x
        new_y = global_config.params['custom_height'] / 2 + new_offset_y

    elif AnchorType.from_string(screen_location) == AnchorType.TOP_RIGHT:
        offset_x = global_config.params['base_width'] - x
        new_x = global_config.params['custom_width'] - offset_x * global_config.scale_uniform
        new_y = y * global_config.scale_y

    elif AnchorType.from_string(screen_location) == AnchorType.BOTTOM_RIGHT:
        # 计算相对于右下角的偏移
        offset_x = global_config.params['base_width'] - x
        offset_y = global_config.params['base_height'] - y

        # 缩放后重新计算位置
        new_x = global_config.params['custom_width'] - offset_x * global_config.scale_uniform
        new_y = global_config.params['custom_height'] - offset_y * global_config.scale_uniform

    return int(new_x), int(new_y), screen_location


# 缩放坐标 todo 优化 合并点与矩形
def scale_corner_anchored(x, y, w, h, screen_location):
    new_x, new_y, new_w, new_h = x, y, w, h
    if global_config.scale_x == global_config.scale_y:
        new_x = x * global_config.scale_uniform
        new_y = y * global_config.scale_uniform
        new_w = w * global_config.scale_uniform
        new_h = h * global_config.scale_uniform

        return int(new_x), int(new_y), int(new_w), int(new_h), screen_location

    if AnchorType.from_string(screen_location) is AnchorType.TOP_LEFT:
        new_x = x * global_config.scale_uniform
        new_y = y * global_config.scale_uniform
        new_w = w * global_config.scale_uniform
        new_h = h * global_config.scale_uniform

    elif AnchorType.from_string(screen_location) is AnchorType.CENTER:
        # 计算相对于底部中央的偏移
        base_center_x = global_config.params['base_width'] / 2
        base_center_y = global_config.params['base_height'] / 2
        offset_x = x - base_center_x
        offset_y = x - base_center_y

        # 缩放偏移
        new_offset_x = offset_x * global_config.scale_uniform
        new_offset_y = offset_y * global_config.scale_uniform
        new_center_x = global_config.params['custom_width'] / 2
        new_center_y = global_config.params['custom_height'] / 2

        # 计算新坐标
        new_x = new_center_x + new_offset_x
        new_y = new_center_y + new_offset_y
        new_w = w * global_config.scale_uniform
        new_h = h * global_config.scale_uniform

    elif AnchorType.from_string(screen_location) is AnchorType.TOP_CENTER:
        # 计算相对于底部中央的偏移
        base_center_x = global_config.params['base_width'] / 2
        offset_x = x - base_center_x

        # 缩放偏移
        new_offset_x = offset_x * global_config.scale_uniform
        new_center_x = global_config.params['custom_width'] / 2

        # 计算新坐标
        new_x = new_center_x + new_offset_x
        new_y = y * global_config.scale_uniform
        new_w = w * global_config.scale_uniform
        new_h = h * global_config.scale_uniform

    elif AnchorType.from_string(screen_location) is AnchorType.TOP_RIGHT:
        offset_x = global_config.params['base_width'] - x

        new_x = global_config.params['custom_width'] - offset_x * global_config.scale_uniform
        new_y = y * global_config.scale_uniform
        new_w = w * global_config.scale_uniform
        new_h = h * global_config.scale_uniform

    elif AnchorType.from_string(screen_location) is AnchorType.BOTTOM_RIGHT:
        # 计算相对于右下角的偏移
        offset_x = global_config.params['base_width'] - x
        offset_y = global_config.params['base_height'] - y

        # 缩放后重新计算位置
        new_x = global_config.params['custom_width'] - offset_x * global_config.scale_uniform
        new_y = global_config.params['custom_height'] - offset_y * global_config.scale_uniform
        new_w = w * global_config.scale_uniform
        new_h = h * global_config.scale_uniform

    elif AnchorType.from_string(screen_location) is AnchorType.BOTTOM_CENTER:
        # 计算相对于底部中央的偏移
        base_center_x = global_config.params['base_width'] / 2
        offset_x = x - base_center_x

        # 缩放偏移
        new_offset_x = offset_x * global_config.scale_uniform
        new_center_x = global_config.params['custom_width'] / 2

        # 缩放后重新计算位置
        new_x = new_center_x + new_offset_x
        new_y = global_config.params['custom_height'] - (
                global_config.params['base_height'] - y) * global_config.scale_uniform
        new_w = w * global_config.scale_uniform
        new_h = h * global_config.scale_uniform

    return int(new_x), int(new_y), int(new_w), int(new_h), screen_location


# 根据缩放因子缩放模板图片
def scale_template(template):
    if template is None:
        return None

    if global_config.scale_x == 1 and global_config.scale_y == 1:
        return template
    if global_config.scale_uniform == 1:
        return template

    new_width = int(template.shape[1] * global_config.scale_uniform)
    new_height = int(template.shape[0] * global_config.scale_uniform)

    if global_config.scale_uniform > 1.0:
        scaled_template = cv2.resize(template, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    else:
        scaled_template = cv2.resize(template, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return scaled_template
