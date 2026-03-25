import threading
import time

import mss

from Action import bucket_full_matched, open_fish_bucket, bucket_48_matched, locked_fish_matched, close_fish_bucket, \
    recognize_fish_quality, lock_fish, discard_fish, bucket_empty_matched, bucket_opened_matched
from GlobalConfig import global_config
from MouseOrKeyBoardUtil import ensure_mouse_left_up, ensure_mouse_right_up, _default_mouse

QUALITY_LEVELS = ["标准", "非凡", "稀有", "史诗", "传奇"]
QUALITY_COLORS = {
    "标准": "⚪",
    "非凡": "🟢",
    "稀有": "🔵",
    "史诗": "🟣",
    "传奇": "🟡"
}

is_auto_fish_discard = 0
discard_level = 1  # 默认不丢弃
discard_count = None

param_lock = threading.Lock()
begin_event = threading.Event()
run_event = threading.Event()


def auto_fish_discard():
    global is_auto_fish_discard, discard_level, run_event, discard_count
    while not begin_event.is_set():
        if run_event.is_set():
            # 确保 mouse 对象已初始化
            if _default_mouse is not None:
                _default_mouse.set_speed(global_config.params['auto_discard_speed'])

            if global_config.scr is None:
                global_config.scr = mss.mss()

            with param_lock:
                is_auto_fish_discard = global_config.params['is_auto_fish_discard']
                discard_level = global_config.params['discard_level']

            if not is_auto_fish_discard:
                print("🌊🐟️ [自动放生] 自动放生开关未打开... 若需要使用此功能，请手动开启开关...")
                run_event.clear()
                continue

            if discard_level == 1:
                print("🌊🐟️ [自动放生] 当前保留普通及以上鱼种，无需丢弃...")
                run_event.clear()
                continue

            try:
                # if not bucket_full_matched():
                #     print("🌊🐟️ [自动放生] 当前桶未满^_^未达到自动放生条件...")
                #     return
                if not bucket_opened_matched():
                    open_fish_bucket()
                    time.sleep(1)

                if bucket_empty_matched():
                    print("🌊🐟️ [自动放生] 鱼桶中没有鱼...")
                    run_event.clear()
                    continue

                while run_event.is_set() :
                    if locked_fish_matched():
                        print("🌊🐟️ [自动放生] 当前没有鱼可以放生...")
                        close_fish_bucket()
                        run_event.clear()
                        break
                    if bucket_48_matched():
                        print("🌊🐟️ [自动放生] 当前鱼桶已满切全部锁住...")
                        close_fish_bucket()
                        run_event.clear()
                        #todo 暂停自动钓鱼线程
                        break

                    level = recognize_fish_quality(50)
                    if level is None:
                        print("🌊🐟️ [自动放生] 未识别出桶中第一条鱼的质量...")
                        run_event.clear()
                        break
                    with param_lock:
                        discard_level = global_config.params['discard_level']
                    print(level)
                    if level < global_config.params['discard_level']:
                        discard_fish()
                        discard_count[level - 1] = discard_count[level - 1] + 1
                        time.sleep(1)
                    else:
                        lock_fish()
                        time.sleep(1)
                count_discard_fish()
            except Exception as e:
                print(f"❌ [错误] 自动放生脚本主循环异常：{e}")
            finally:
                # 确保 mss 资源被正确释放
                if global_config.scr is not None:
                    try:
                        global_config.scr.close()
                    except:
                        pass
                    global_config.scr = None
        time.sleep(1)


def count_discard_fish():
    global discard_count
    print(f"🌊🐟️ [自动放生] 本次放鱼结束..共释放如下")
    for i in range(4):
        emoji = QUALITY_COLORS.get(QUALITY_LEVELS[i])
        print(f"🌊🐟️ {emoji} {QUALITY_LEVELS[i]}: 释放{discard_count[i]}条")
    return 0


def toggle_run_auto_fish_discard():
    global run_event, discard_count
    with param_lock:
        global_config.auto_fish_discard_thread_event = run_event
    if run_event.is_set():
        run_event.clear()  # 暂停
        ensure_mouse_left_up()
        ensure_mouse_right_up()
        count_discard_fish()
        print("⏸️  [状态] 放鱼脚本已暂停")
    else:
        discard_count = [0, 0, 0, 0]
        run_event.set()  # 恢复运行
