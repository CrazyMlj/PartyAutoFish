import threading
import time

import mss

from Action import f1_matched, f2_matched, fishing_matched, overtime_matched, overtime_y, bait_match_val, overtime_n, \
    fished_matched, bucket_full_matched
from AutoFishDiscard import auto_fish_discard_sync
from FishRecord import record_caught_fish, end_current_session, start_new_session
from GlobalConfig import global_config
from MouseOrKeyBoardUtil import hold_mouse_left_button, press_and_release_mouse_button, ensure_mouse_left_up

run_event = threading.Event()
begin_event = threading.Event()

previous_result = None  # 上次识别的结果
current_result = 0  # 当前识别的数字
reel_rod_times = 0  # 当前收杆次数


def compare_results():
    global current_result, previous_result
    if current_result is None or previous_result is None:
        return 0  # 无法比较，返回 0 作为标识
    if current_result > previous_result:
        return 1  # 当前结果较大
    elif current_result < previous_result:
        return -1  # 上次结果较大
    else:
        return 0  # 当前结果与上次相同


def auto_fish():
    """
    自动钓鱼主函数（线程安全版本）
    每个线程使用独立的 mss 实例，避免资源竞争
    """
    global previous_result, current_result, reel_rod_times

    # 每个线程使用独立的 mss 实例
    local_scr = None

    while not begin_event.is_set():
        if run_event.is_set():
            # 检查是否需要暂停（丢鱼进行中）
            if global_config._fishing_pause_event.is_set():
                time.sleep(0.5)
                continue

            try:
                # 创建独立的 mss 实例
                if local_scr is None:
                    local_scr = mss.mss()
                global_config.set_scr(local_scr)
                # 检测 F1/F2 抛竿
                if f1_matched() or f2_matched():
                    hold_mouse_left_button(global_config.get_param('casting_time'))
                    if bucket_full_matched():
                        ensure_mouse_left_up()
                        print("🌊🐟️ [自动放生] 桶已钓满...")
                        # 调用同步丢鱼函数，会设置暂停事件
                        auto_fish_discard_sync(run_event)
                        continue
                    time.sleep(0.15)
                elif fishing_matched():
                    hold_mouse_left_button(0.3)

                time.sleep(0.05)

                overtime_action()

                # 获取当前结果（线程安全）
                bait_result = bait_match_val()
                if bait_result is not None:
                    current_result = global_config.get_bait_count()
                else:
                    current_result = previous_result if previous_result is not None else 0
                    time.sleep(0.1)
                    continue

                # 比较并执行操作
                comparison_result = compare_results()
                time.sleep(0.01)

                if comparison_result == -1:  # 当前结果小于上次结果
                    previous_result = current_result  # 更新上次识别的结果

                    # 线程安全地读取最大拉杆次数
                    current_times = global_config.get_param('cycle_times')

                    while not fished_matched() and run_event.is_set():
                        # 检查是否应该暂停（丢鱼进行中）
                        if global_config._fishing_pause_event.is_set():
                            break

                        if reel_rod_times <= current_times:
                            reel_rod_times += 1
                            press_and_release_mouse_button()  # 执行点击循环直到识别到 star.png
                            # 拉鱼过程中出现加时
                            overtime_action()
                        else:
                            reel_rod_times = 0
                            print("🎣 [提示] 达到最大拉杆次数，本轮结束")
                            break
                    ensure_mouse_left_up()
                    reel_rod_times = 0

                    # 钓到鱼后，识别并记录鱼的信息
                    try:
                        record_caught_fish()
                    except Exception as e:
                        print("⚠️  [警告] 记录鱼信息失败：{}".format(e))

                elif comparison_result == 1:
                    previous_result = current_result

            except Exception as e:
                print("❌ [错误] 钓鱼脚本主循环异常：{}".format(e))

        time.sleep(0.1)

    # 清理资源
    if local_scr is not None:
        try:
            local_scr.close()
        except:
            pass


# 加时
def overtime_action():
    global previous_result
    # 处理加时选择（线程安全读取参数）
    current_overtime_val = global_config.get_param('is_overtime')
    if current_overtime_val == 0:
        if overtime_matched():
            overtime_n()
            if bait_match_val() is not None:
                previous_result = global_config.get_bait_count()
    elif current_overtime_val == 1:
        if overtime_matched():
            overtime_y()
            if bait_match_val() is not None:
                previous_result = global_config.get_bait_count()
    time.sleep(0.05)


def toggle_run_auto_fish():
    """
    切换自动钓鱼运行状态（线程安全）
    """
    global reel_rod_times, previous_result, run_event

    # 注册事件对象
    with global_config._global_lock:
        global_config.auto_fish_thread_event = run_event

    if run_event.is_set():
        run_event.clear()  # 暂停
        reel_rod_times = 0
        previous_result = None
        ensure_mouse_left_up()  # 确保鼠标没有按下
        end_current_session()  # 结束钓鱼会话
        print("⏸️  [状态] 钓鱼脚本已暂停")
    else:
        start_new_session()  # 开始新的钓鱼会话
        if previous_result is None:
            temp_scr = None
            try:
                temp_scr = mss.mss()
                global_config.set_scr(temp_scr)
                bait_result = bait_match_val()
                if bait_result is not None and bait_result >= 0:
                    previous_result = global_config.get_bait_count()
                    run_event.set()  # 恢复运行
                    print("▶️  [状态] 钓鱼脚本开始运行")
                else:
                    time.sleep(0.1)
                    print("⚠️  [警告] 未识别到鱼饵，请确保游戏界面正确")
            except Exception as e:
                print("❌ [错误] 钓鱼脚本初始化失败：{}".format(e))
            finally:
                if temp_scr is not None:
                    try:
                        temp_scr.close()
                    except:
                        pass
        else:
            run_event.set()
            print("▶️  [状态] 钓鱼脚本继续运行")
