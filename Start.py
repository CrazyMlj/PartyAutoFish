# =========================
# 程序入口 - 多线程优化版本
# =========================
import threading
import time
from pynput import keyboard as pynput_keyboard

from Action import png_template
from AutoFish import toggle_run_auto_fish, auto_fish
from AutoFishDiscard import auto_fish_discard, toggle_run_auto_fish_discard
from AutoUNO import toggle_run_auto_uno, auto_uno_skip
from AutoWait import toggle_run_auto_await, auto_await
from FishRecord import load_all_fish_records
from GUI import create_gui
from GlobalConfig import global_config

listener_f2 = None  # 监听
listener_f3 = None  # 监听
listener_f4 = None  # 监听
listener_f5 = None  # 监听

# 全局标志
templates_loaded = False
initialization_complete = False
threads = None


def on_press_f2(key):
    time.sleep(0.02)
    if key == pynput_keyboard.Key.f2:
        if global_config.auto_fish_discard_thread_event is not None:
            if global_config.auto_fish_discard_thread_event.is_set():
                toggle_run_auto_fish_discard()  # 暂停自动丢鱼
        if global_config.auto_await_thread_event is not None:
            if global_config.auto_await_thread_event.is_set():
                toggle_run_auto_await()  # 暂停自动挂机
        if global_config.auto_uno_thread_event is not None:
            if global_config.auto_uno_thread_event.is_set():
                toggle_run_auto_uno()  # 暂停uno自动跳过
        # 暂停或恢复程序
        toggle_run_auto_fish()


def on_press_f3(key):
    time.sleep(0.02)
    if key == pynput_keyboard.Key.f3:
        if global_config.auto_fish_thread_event is not None:
            if global_config.auto_fish_thread_event.is_set():
                toggle_run_auto_fish()  # 暂停自动钓鱼
        if global_config.auto_await_thread_event is not None:
            if global_config.auto_await_thread_event.is_set():
                toggle_run_auto_await()  # 暂停自动挂机
        if global_config.auto_uno_thread_event is not None:
            if global_config.auto_uno_thread_event.is_set():
                toggle_run_auto_uno()  # 暂停uno自动跳过
        # 暂停或恢复程序
        toggle_run_auto_fish_discard()


def on_press_f4(key):
    time.sleep(0.02)
    if key == pynput_keyboard.Key.f4:
        if global_config.auto_fish_discard_thread_event is not None:
            if global_config.auto_fish_discard_thread_event.is_set():
                toggle_run_auto_fish_discard()  # 暂停自动丢鱼
        if global_config.auto_fish_thread_event is not None:
            if global_config.auto_fish_thread_event.is_set():
                toggle_run_auto_fish()  # 暂停自动钓鱼
        if global_config.auto_uno_thread_event is not None:
            if global_config.auto_uno_thread_event.is_set():
                toggle_run_auto_uno()  # 暂停uno自动跳过
        # 暂停或恢复程序
        toggle_run_auto_await()


def on_press_f5(key):
    time.sleep(0.02)
    if key == pynput_keyboard.Key.f5:
        if global_config.auto_fish_discard_thread_event is not None:
            if global_config.auto_fish_discard_thread_event.is_set():
                toggle_run_auto_fish_discard()  # 暂停自动丢鱼
        if global_config.auto_fish_thread_event is not None:
            if global_config.auto_fish_thread_event.is_set():
                toggle_run_auto_fish()  # 暂停自动钓鱼
        if global_config.auto_await_thread_event is not None:
            if global_config.auto_await_thread_event.is_set():
                toggle_run_auto_await()  # 暂停自动挂机
        # 暂停或恢复程序
        toggle_run_auto_uno()


def start_hotkey_listener():
    global listener_f2, listener_f3, listener_f4, listener_f5
    if listener_f2 is None or not listener_f2.running:
        listener_f2 = pynput_keyboard.Listener(on_press=on_press_f2)
        listener_f2.daemon = True
        listener_f2.start()

    if listener_f3 is None or not listener_f3.running:
        listener_f3 = pynput_keyboard.Listener(on_press=on_press_f3)
        listener_f3.daemon = True
        listener_f3.start()

    if listener_f4 is None or not listener_f4.running:
        listener_f4 = pynput_keyboard.Listener(on_press=on_press_f4)
        listener_f4.daemon = True
        listener_f4.start()

    if listener_f5 is None or not listener_f5.running:
        listener_f5 = pynput_keyboard.Listener(on_press=on_press_f5)
        listener_f5.daemon = True
        listener_f5.start()


def load_templates_async():
    """异步加载图像模板（在后台线程执行）"""
    global templates_loaded
    try:
        print("🖼️[后台加载] 正在加载图像模板...")
        png_template.load_templates()
        templates_loaded = True
        print("✅[后台加载] 模板加载完成")
    except Exception as e:
        print("❌ [错误] 模板加载失败：{}".format(e))
        templates_loaded = False


def init_worker_threads():
    """延迟启动工作线程（在 GUI 就绪后执行）"""
    global initialization_complete, threads

    # 等待模板加载完成
    while not templates_loaded:
        time.sleep(0.1)

    threads = []
    # 初始化工作线程
    auto_fish_thread = threading.Thread(target=auto_fish, daemon=True)
    threads.append(auto_fish_thread)

    auto_fish_discard_thread = threading.Thread(target=auto_fish_discard, daemon=True)
    threads.append(auto_fish_discard_thread)

    auto_await_thread = threading.Thread(target=auto_await, daemon=True)
    threads.append(auto_await_thread)

    auto_uno_skip_thread = threading.Thread(target=auto_uno_skip, daemon=True)
    threads.append(auto_uno_skip_thread)

    initialization_complete = True


def on_gui_ready():
    """GUI 就绪后的回调函数"""
    global threads
    # 在 GUI 主线程中启动工作线程
    for thread in threads:
        thread.start()
    print("✨ [就绪] 所有工作线程已启动")


if __name__ == "__main__":
    print()
    print("=" * 63)
    print("  PartyFish 自动钓鱼助手  v5.5")
    print("=" * 63)
    print("  快捷键：F2 启动/暂停钓鱼 | F3 启动/暂停放鱼")
    print("  快捷键：F4 启动/暂停挂机 | F5 启动/暂停uno自动跳过")
    print("=" * 63)
    print()

    # 【优化 1】快速加载配置（同步）
    print("📦 加载配置文件...")
    start_time = time.time()
    global_config.load_parameters()
    print("✅ 配置加载完成 ({:.2f}s)".format(time.time() - start_time))

    # 【优化 2】快速加载钓鱼记录（同步）
    print("📊 加载钓鱼记录...")
    start_time = time.time()
    load_all_fish_records()
    print("✅ 记录加载完成 ({:.2f}s)".format(time.time() - start_time))

    # 【优化 3】异步加载图像模板（后台线程）
    print("🖼️ 异步加载图像模板...")
    template_thread = threading.Thread(target=load_templates_async, daemon=True)
    template_thread.start()

    # 【优化 4】快速启动热键监听（不等待模板加载）
    print("🎮 启动热键监听...")
    start_time = time.time()
    start_hotkey_listener()
    print("✅ 热键监听已启动 ({:.2f}s)".format(time.time() - start_time))

    init_worker_threads()

    # 创建 GUI 并注册就绪回调
    create_gui(on_ready_callback=on_gui_ready)
