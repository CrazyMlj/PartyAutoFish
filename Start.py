# =========================
# 程序入口
# =========================
import threading
import time

import keyboard
import mss
from pynput import keyboard

from Action import png_template
from AutoFish import toggle_run_auto_fish, auto_fish
from AutoFishDiscard import auto_fish_discard, toggle_run_auto_fish_discard
from FishRecord import load_all_fish_records
from GUI import create_gui
from GlobalConfig import global_config
from MouseOrKeyBoardUtil import HumanLikeMouse

listener_f2 = None  # 监听
listener_f3 = None  # 监听


def on_press_f2(key):
    time.sleep(0.02)
    if key == keyboard.Key.f2:
        if global_config.auto_fish_discard_thread_event is not None:
            if global_config.auto_fish_discard_thread_event.is_set():
                toggle_run_auto_fish_discard()  # 暂停
        # 暂停或恢复程序
        toggle_run_auto_fish()
    return


def on_press_f3(key):
    time.sleep(0.02)
    if key == keyboard.Key.f3:
        if global_config.auto_fish_thread_event is not None:
            if global_config.auto_fish_thread_event.is_set():
                toggle_run_auto_fish()  # 暂停
        # 暂停或恢复程序
        toggle_run_auto_fish_discard()
        return


def start_hotkey_listener():
    global listener_f2, listener_f3
    if listener_f2 is None or not listener_f2.running:
        listener_f2 = keyboard.Listener(on_press=on_press_f2)
        listener_f2.daemon = True
        listener_f2.start()

    if listener_f3 is None or not listener_f3.running:
        listener_f3 = keyboard.Listener(on_press=on_press_f3)
        listener_f3.daemon = True
        listener_f3.start()


if __name__ == "__main__":
    print()
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 50 + "║")
    print("║     🎣  PartyFish 自动钓鱼助手  v4.3             ║")
    print("║" + " " * 50 + "║")
    print("╠" + "═" * 50 + "╣")
    print(
        f"║  📺 当前分辨率: {global_config.params['custom_width']} × {global_config.params['custom_height']}".ljust(
            45) + "║")
    print("║  ⌨️ 快捷键: F2 启动/暂停钓鱼脚本                 ║")
    print("║  ⌨️ 快捷键: F3 启动/暂停放鱼脚本                 ║")
    print("║  🔧 开发者: Crazy                                ║")
    print("╚" + "═" * 50 + "╝")
    print()

    # 加载参数和模板
    print("📦 [初始化] 正在加载配置...")
    global_config.load_parameters()

    # 加载历史钓鱼记录
    print("📊 [初始化] 正在加载钓鱼记录...")
    load_all_fish_records()

    print("🖼️  [初始化] 正在加载图像模板...")
    png_template.load_templates()
    print("✅ [初始化] 模板加载完成")

    # 启动热键监听
    print("🎮 [初始化] 正在启动热键监听...")
    start_hotkey_listener()
    print("✅ [初始化] 热键监听已启动")

    print()
    print("┌" + "─" * 63 + "┐")
    print("│  🚀 程序已就绪，按 F2 开始自动钓鱼! 按 F3 开始自动丢鱼!       │")
    print("└" + "─" * 63 + "┘")
    print()

    # 将auto_fish()放在后台线程运行（daemon=True确保主线程退出时自动结束）
    auto_fish_thread = threading.Thread(target=auto_fish, daemon=True)
    auto_fish_thread.start()

    auto_fish_discard_thread = threading.Thread(target=auto_fish_discard, daemon=True)
    auto_fish_discard_thread.start()

    # GUI必须在主线程运行（Tkinter要求）
    # 这样可以确保GUI正常工作且不会崩溃
    create_gui()
