# 新增uno刷牌自动跳过功能 todo


from Action import uno_skip_matched, uno_click_skip_button
from GlobalConfig import global_config

skip_times = 0


# 自动跳过至摸到35张
def uno_skip_insure():
    global skip_times

    uno_skip_times = global_config.get_param('uno_skip_times')

    while True:
        if uno_skip_times <= 0:
            break

        if skip_times == uno_skip_times:
            break

        if uno_skip_matched():
            skip_times += 1
            uno_click_skip_button()


# 一直跳过
def uno_skip_allways():
    while True:
        if uno_skip_matched():
            uno_click_skip_button()
