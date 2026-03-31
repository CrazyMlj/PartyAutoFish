# 自动挂机 todo
import random

from MouseOrKeyBoardUtil import hold_mouse_left_button, hold_mouse_right_button, key_press

actions = ['mouse_left', 'mouse_right', 'key_w.0x57', 'key_a.0x41', 'key_s.0x53', 'key_d.0x44', 'key_space.0x20']


def auto_wait():
    global actions
    action_choice = random.choice(actions)
    if 'mouse' in action_choice:
        if action_choice == 'mouse_left':
            hold_mouse_left_button(0.1)
        elif action_choice == 'mouse_right':
            hold_mouse_right_button(0.1)

    elif 'key' in action_choice:
        key = action_choice.split('.')[1]
        key_press(key, 0.1)

