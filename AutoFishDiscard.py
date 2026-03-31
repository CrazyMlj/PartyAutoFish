import threading
import time

import mss

from Action import open_fish_bucket, locked_fish_matched, close_fish_bucket, \
    recognize_fish_quality, lock_fish, discard_fish, bucket_empty_matched, bucket_opened_matched, mouse_move_safe, \
    waiting_strike_matched, retrieve_the_rod, drag_fish_matched, bucket_48_matched, fished_matched
from GlobalConfig import global_config
from MouseOrKeyBoardUtil import ensure_mouse_left_up, ensure_mouse_right_up, _default_mouse, hold_mouse_left_button

QUALITY_LEVELS = ["标准", "非凡", "稀有", "史诗", "传奇"]
QUALITY_COLORS = {
    "标准": "⚪",
    "非凡": "🟢",
    "稀有": "🔵",
    "史诗": "🟣",
    "传奇": "🟠"
}

is_auto_fish_discard = 0
discard_level = 1  # 默认不丢弃
discard_count = None

run_event = threading.Event()


def auto_fish_discard_sync(event):
    """
    同步自动丢鱼函数（线程安全版本）
    会设置钓鱼暂停事件，确保丢鱼期间钓鱼线程暂停
    """
    global is_auto_fish_discard, discard_level, discard_count

    # 通知钓鱼线程暂停
    global_config._fishing_pause_event.set()

    discard_count = [0, 0, 0, 0]

    # 使用独立的 mss 实例
    local_scr = None

    try:
        # 创建独立的 mss 实例
        if local_scr is None:
            local_scr = mss.mss()
        global_config.set_scr(local_scr)

        with global_config._params_lock:
            is_auto_fish_discard = global_config.params['is_auto_fish_discard']
            discard_level = global_config.params['discard_level']

        if not is_auto_fish_discard:
            print("🌊🐟️ [放生] 自动放生开关未打开... 若需要使用此功能，请手动开启开关...")
            return

        if discard_level == 1:
            print("🌊🐟️ [放生] 当前保留普通及以上鱼种，无需丢弃...")
            return

        if not bucket_opened_matched():
            open_fish_bucket()
            time.sleep(2)

        if bucket_empty_matched():
            print("🌊🐟️ [放生] 鱼桶中没有鱼...")
            return

        while event.is_set():
            if locked_fish_matched():
                print("🌊🐟️ [放生] 当前没有鱼可以放生...")

                # 等待屏幕变化
                time.sleep(1)

                # 鱼桶已满
                if bucket_48_matched():
                    print("🌊🐟️[放生] 桶里已有48条鱼...")
                    print("⏸️  [状态] 钓鱼脚本已暂停")
                    # 钓鱼程序暂停
                    event.clear()

                close_fish_bucket()
                break

            # 将鼠标移走排除鱼品质判断干扰
            mouse_move_safe()

            level = recognize_fish_quality()
            if level is None:
                print("🌊🐟️ [放生] 未识别出桶中第一条鱼的质量...")
                continue

            with global_config._params_lock:
                discard_level = global_config.params['discard_level']

            if level < global_config.params['discard_level']:
                discard_fish()
                discard_count[level - 1] = discard_count[level - 1] + 1
            else:
                lock_fish()

        count_discard_fish()
        time.sleep(1)

    except Exception as e:
        print("❌ [错误] 自动放生脚本主循环异常：{}".format(e))
    finally:
        # 确保丢鱼完成后，通知钓鱼线程继续
        global_config._fishing_pause_event.clear()

        # 清理资源
        if local_scr is not None:
            try:
                local_scr.close()
            except:
                pass


def auto_fish_discard():
    """
    自动丢鱼主函数（线程安全版本）
    每个线程使用独立的 mss 实例，避免资源竞争
    """
    global is_auto_fish_discard, discard_level, run_event, discard_count

    # 每个线程使用独立的 mss 实例
    local_scr = None

    while True:
        if run_event.is_set():
            try:
                # 暂停自动钓鱼
                global_config._fishing_pause_event.set()

                # 创建独立的 mss 实例
                if local_scr is None:
                    local_scr = mss.mss()
                global_config.set_scr(local_scr)

                with global_config._params_lock:
                    is_auto_fish_discard = global_config.params['is_auto_fish_discard']
                    discard_level = global_config.params['discard_level']

                if not is_auto_fish_discard:
                    print("🌊🐟️ [放生] 自动放生开关未打开... 若需要使用此功能，请手动开启开关...")
                    stop_discard_fish()
                    continue

                if discard_level == 1:
                    print("🌊🐟️ [放生] 当前保留普通及以上鱼种，无需丢弃...")
                    stop_discard_fish()
                    continue

                # 前置判断
                # 是否在拉杆阶段
                if drag_fish_matched():
                    print("🌊🐟️ [放生] 当前正在拉鱼无法自动放生...")
                    stop_discard_fish()
                    continue

                # 是否在等待上鱼阶段
                if waiting_strike_matched():
                    retrieve_the_rod()
                    time.sleep(3.5)

                # 是否在钓鱼完成界面
                if fished_matched():
                    hold_mouse_left_button(0.2)
                    time.sleep(1)

                # 鱼桶是否已打开
                if not bucket_opened_matched():
                    open_fish_bucket()
                    time.sleep(2)

                if bucket_empty_matched():
                    print("🌊🐟️ [放生] 鱼桶中没有鱼...")
                    stop_discard_fish()
                    continue

                while run_event.is_set():
                    if locked_fish_matched():
                        print("🌊🐟️ [放生] 当前没有鱼可以放生...")
                        close_fish_bucket()
                        stop_discard_fish()
                        break

                    # 将鼠标移走排除鱼品质判断干扰
                    mouse_move_safe()

                    level = recognize_fish_quality()
                    if level is None:
                        print("🌊🐟️ [放生] 未识别出桶中第一条鱼的质量...")
                        stop_discard_fish()
                        break

                    with global_config._params_lock:
                        discard_level = global_config.params['discard_level']

                    if level < discard_level:
                        discard_fish()
                        discard_count[level - 1] += 1
                    else:
                        lock_fish()
                time.sleep(1)
                count_discard_fish()

            except Exception as e:
                print("❌ [错误] 自动放生脚本主循环异常：{}".format(e))
            finally:
                # 通知钓鱼线程继续
                global_config._fishing_pause_event.clear()
                # 清理资源（注意：不在这里关闭 local_scr，因为循环还要继续）
                pass

        time.sleep(1)

    # 最终清理资源
    if local_scr is not None:
        try:
            local_scr.close()
        except:
            pass


def count_discard_fish():
    global discard_count
    print("🌊🐟️ [放生] 本次放鱼结束..共释放如下")
    for i in range(4):
        emoji = QUALITY_COLORS.get(QUALITY_LEVELS[i])
        print("🌊🐟️ {} {}: 释放{}条".format(emoji, QUALITY_LEVELS[i], discard_count[i]))
    return 0


def toggle_run_auto_fish_discard():
    """
    切换自动丢鱼运行状态（线程安全）
    """
    global run_event, discard_count

    # 注册事件对象
    with global_config._global_lock:
        global_config.auto_fish_discard_thread_event = run_event

    if run_event.is_set():
        stop_discard_fish()
        count_discard_fish()
        print("⏸️  [状态] 放鱼脚本已暂停")
    else:
        discard_count = [0, 0, 0, 0]
        run_event.set()  # 恢复运行
        print("▶️  [状态] 放鱼脚本开始运行")


def stop_discard_fish():
    run_event.clear()  # 暂停
    ensure_mouse_left_up()
    ensure_mouse_right_up()
    print("⏸️  [状态] 放鱼脚本已暂停")