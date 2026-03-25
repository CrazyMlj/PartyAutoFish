import threading
import time

import mss

from Action import f1_matched, f2_matched, fishing_matched, overtime_matched, overtime_y, bait_math_val, overtime_n, \
    fished_match
from FishRecord import record_caught_fish, end_current_session, start_new_session
from GlobalConfig import global_config
from MouseOrKeyBoardUtil import hold_mouse_left_button, press_and_release_mouse_button, ensure_mouse_left_up

run_event = threading.Event()
begin_event = threading.Event()

param_lock = threading.Lock()
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
    global param_lock, run_event, begin_event, previous_result, current_result, reel_rod_times
    while not begin_event.is_set():
        if run_event.is_set():
            global_config.scr = None
            try:
                global_config.scr = mss.mss()

                # 检测F1/F2抛竿
                if f1_matched():
                    hold_mouse_left_button(global_config.params['casting_time'])
                    time.sleep(0.15)
                elif f2_matched():
                    hold_mouse_left_button(global_config.params['casting_time'])
                    time.sleep(0.15)
                elif fishing_matched():
                    hold_mouse_left_button(global_config.params['casting_time'])

                time.sleep(0.05)

                # 处理加时选择（使用锁保护读取is_overtime）
                with param_lock:
                    current_overtime_val = global_config.params['is_overtime']

                if current_overtime_val == 0:
                    if overtime_matched():
                        overtime_y()
                        if bait_math_val():
                            previous_result = global_config.bait_count_val
                elif current_overtime_val == 1:
                    if overtime_matched():
                        overtime_n()
                        if bait_math_val():
                            previous_result = global_config.bait_count_val
                time.sleep(0.05)

                # 获取当前结果
                if bait_math_val():
                    current_result = global_config.bait_count_val
                else:
                    current_result = previous_result  # 将当前数字设为上次的数字
                    time.sleep(0.1)
                    continue  # 会在finally中关闭scr
                # 比较并执行操作
                comparison_result = compare_results()
                time.sleep(0.01)

                if comparison_result == -1:  # 当前结果小于上次结果
                    previous_result = current_result  # 更新上次识别的结果
                    while not fished_match() and run_event.is_set():
                        # 使用锁保护读取times
                        with param_lock:
                            current_times = global_config.params['cycle_times']
                        if reel_rod_times <= current_times:
                            reel_rod_times += 1
                            press_and_release_mouse_button()  # 执行点击循环直到识别到 star.png
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
                        print(f"⚠️  [警告] 记录鱼信息失败: {e}")

                elif comparison_result == 1:
                    previous_result = current_result
                    # continue会在finally中关闭scr

            except Exception as e:
                print(f"❌ [错误] 钓鱼脚本主循环异常: {e}")
            finally:
                # 确保mss资源被正确释放
                if global_config.scr is not None:
                    try:
                        global_config.scr.close()
                    except:
                        pass
                    global_config.scr = None
        time.sleep(0.1)


def toggle_run_auto_fish():
    global reel_rod_times, previous_result,run_event
    with param_lock:
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
                global_config.scr = temp_scr  # 临时赋值供bait_math_val使用
                bait_result = bait_math_val()
                if bait_result or bait_result == 0:
                    previous_result = global_config.bait_count_val
                    run_event.set()  # 恢复运行
                    print("▶️  [状态] 钓鱼脚本开始运行")
                else:
                    time.sleep(0.1)
                    print("⚠️  [警告] 未识别到鱼饵，请确保游戏界面正确")
            except Exception as e:
                print(f"❌ [错误] 钓鱼脚本初始化失败: {e}")
            finally:
                if temp_scr is not None:
                    try:
                        temp_scr.close()
                    except:
                        pass
                scr = None
        else:
            run_event.set()
            print("▶️  [状态] 钓鱼脚本继续运行")
