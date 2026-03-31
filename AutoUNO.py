# 新增uno刷牌自动跳过功能
import threading
import time

import mss

from Action import uno_skip_matched, uno_click_skip_button
from GlobalConfig import global_config
from MouseOrKeyBoardUtil import ensure_mouse_left_up

skip_times = 0
run_event = threading.Event()


# 自动跳过至摸到35张
def auto_uno_skip():
    global skip_times

    uno_skip_times = global_config.get_param('uno_skip_times')
    is_keep_skipping = global_config.get_param('is_keep_skipping')

    local_scr = None


    while True:
        if not run_event.is_set():
            run_event.wait(timeout=1.0)  # 等待 1 秒，避免死锁
            continue

        try:
            # 创建独立的 mss 实例
            if local_scr is None:
                local_scr = mss.mss()
            global_config.set_scr(local_scr)

            if run_event.is_set():
                if uno_skip_times <= 0:
                    stop_auto_skip()
                    break

                if not is_keep_skipping:
                    if skip_times >= uno_skip_times:
                        stop_auto_skip()
                        break

                if uno_skip_matched():
                    skip_times += 1
                    uno_click_skip_button()
                    time.sleep(1.5)
            time.sleep(0.2)
        except Exception as e:
            print("⚠️  [警告] uno自动跳过操作失败：{}".format(e))


def toggle_run_auto_uno():
    global run_event, skip_times

    # 注册事件对象
    with global_config._global_lock:
        global_config.auto_uno_thread_event = run_event

    if run_event.is_set():
        run_event.clear()  # 暂停
        stop_auto_skip()
    else:
        skip_times = 7 # 初始牌为7张
        run_event.set()
        print("▶️  [状态] uno跳过脚本开始运行")


def stop_auto_skip():
    ensure_mouse_left_up()
    print("⏸️  [状态] uno跳过脚本已暂停")
