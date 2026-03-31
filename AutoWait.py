# 自动挂机
import random
import threading
import time

from GlobalConfig import global_config
from MouseOrKeyBoardUtil import hold_mouse_left_button, hold_mouse_right_button, key_press, ensure_mouse_left_up, \
    ensure_mouse_right_up, key_release

actions = ['mouse_left', 'mouse_right', 'key_w.0x57', 'key_a.0x41', 'key_s.0x53', 'key_d.0x44', 'key_space.0x20']

begin_event = threading.Event()
run_event = threading.Event()


def auto_await():
    global actions, run_event

    while not begin_event.is_set():
        while run_event.is_set():
            action_choice = random.choice(actions)
            if 'mouse' in action_choice:
                if action_choice == 'mouse_left':
                    hold_mouse_left_button(0.1)
                    print("🎮 [挂机] 操作鼠标左键")
                elif action_choice == 'mouse_right':
                    hold_mouse_right_button(0.1)
                    print("🎮 [挂机] 操作鼠标右键")

            elif 'key' in action_choice:
                key_split = action_choice.split('.')
                key = key_split[1]
                key_press(key, 0.1)
                print("🎮 [挂机] 操作{}".format(key_split[0].split('_')[1]))
            time.sleep(180)


def toggle_run_auto_await():
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
