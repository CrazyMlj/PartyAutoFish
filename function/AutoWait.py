# 自动挂机
import random
import threading
import time

from config.GlobalConfig import global_config
from utils.MouseOrKeyBoardUtil import hold_mouse_left_button, hold_mouse_right_button, key_press, ensure_mouse_left_up, \
    ensure_mouse_right_up, key_release

actions = ['mouse_left', 'mouse_right', 'key_w.0x57', 'key_a.0x41', 'key_s.0x53', 'key_d.0x44', 'key_space.0x20']

run_event = threading.Event()


def auto_await():
    """
    自动挂机主函数
    """
    global actions, run_event

    while True:
        # 等待启动信号（阻塞式等待，不占用 CPU）
        if not run_event.is_set():
            run_event.wait(timeout=1.0)  # 等待 1 秒，避免死锁
            continue

        # 执行一次随机操作
        action_choice = random.choice(actions)
        try:
            if 'mouse' in action_choice:
                if action_choice == 'mouse_left':
                    hold_mouse_left_button(0.1)
                    print("🎮 [挂机] 操作鼠标左键")
                elif action_choice == 'mouse_right':
                    hold_mouse_right_button(0.1)
                    print("🎮 [挂机] 操作鼠标右键")

            elif 'key' in action_choice:
                key_split = action_choice.split('.')
                key = int(key_split[1], 16)
                key_press(key, 0.1)
                print("🎮 [挂机] 操作{}".format(key_split[0].split('_')[1]))
        except Exception as e:
            print("⚠️  [警告] 挂机操作失败：{}".format(e))

        # 长时间休眠（180 秒）
        # 使用分段休眠，以便快速响应停止信号
        for _ in range(180):  # 180 次 * 1 秒 = 180 秒
            if not run_event.is_set():
                continue
            time.sleep(1.0)


def toggle_run_auto_await():
    """切换自动挂机运行状态（线程安全）"""
    global run_event

    # 注册事件对象
    with global_config._global_lock:
        global_config.auto_await_thread_event = run_event

    if run_event.is_set():
        run_event.clear()  # 暂停
        release_mouse_and_keyboard()
        print("⏸️  [状态] 挂机脚本已暂停")
    else:
        run_event.set()
        print("▶️  [状态] 挂机脚本开始运行")


def release_mouse_and_keyboard():
    """释放所有按下的鼠标和键盘"""
    global actions
    for action in actions:
        if 'mouse' in action:
            if action == 'mouse_left':
                ensure_mouse_left_up()
            elif action == 'mouse_right':
                ensure_mouse_right_up()

        elif 'key' in action:
            key = action.split('.')[1]
            key_release(key)
