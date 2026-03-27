import json
import threading

QUALITY_LEVEL = ["标准", "非凡", "稀有", "史诗", "传奇"]
QUALITY_LEVEL_MAP = {
    "标准": 1,
    "非凡": 2,
    "稀有": 3,
    "史诗": 4,
    "传奇": 5
}

# 参数文件路径
PARAMETER_FILE = "./parameters.json"


class GlobalConfig:
    # 全局配置单例
    _instance = None
    # 单例锁
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.scale_uniform = 1.0
        self.scr = None
        self.gui_fish_update_callback = None
        self.bait_count_val = None
        self.auto_fish_thread_event = None
        self.auto_fish_discard_thread_event = None
        self.mouse = None
        self.params = {
            'interval': 0.4,
            'mouse_left_hold_time': 1.8,
            'mouse_left_release_time': 0.7,
            'cycle_times': 20.0,
            'casting_time': 1.65,
            'is_overtime': 1,
            'is_auto_fish_discard': 0,
            'auto_discard_speed': 0.4,
            'discard_level': 4,
            'resolution': '2K',
            'custom_width': 2560,
            'custom_height': 1440,
            'base_width': 2560,
            'base_height': 1440
        }

        # 线程同步原语 - 统一管理所有锁
        self._global_lock = threading.RLock()  # 可重入锁，用于全局状态
        self._scr_lock = threading.Lock()  # 专门保护 scr 资源
        self._bait_count_lock = threading.Lock()  # 专门保护 bait_count_val
        self._params_lock = threading.RLock()  # 保护 params 字典
        self._mouse_lock = threading.Lock()  # 保护鼠标操作

        # 线程协调事件
        self._fishing_pause_event = threading.Event()  # 钓鱼暂停事件（丢鱼时）
        self._initialized = True

    def update(self, **kwargs):
        # 批量更新参数（线程安全）
        with self._params_lock:
            for key, value in kwargs.items():
                if key in self.params:
                    self.params[key] = value
        self.save_parameters()

    def get_param(self, key):
        """线程安全地获取参数"""
        with self._params_lock:
            return self.params.get(key)

    def update_param(self, key, value):
        """线程安全地更新单个参数"""
        with self._params_lock:
            self.params[key] = value

    def get_bait_count(self):
        """线程安全地获取鱼饵数量"""
        with self._bait_count_lock:
            return self.bait_count_val

    def set_bait_count(self, value):
        """线程安全地设置鱼饵数量"""
        with self._bait_count_lock:
            self.bait_count_val = value

    def get_scr(self):
        """线程安全地获取截图对象"""
        with self._scr_lock:
            return self.scr

    def set_scr(self, value):
        """线程安全地设置截图对象"""
        with self._scr_lock:
            self.scr = value

    def save_parameters(self):
        global QUALITY_LEVEL_MAP
        with self._params_lock:
            data = self.params.copy()
        self.scale_x = data.get('custom_width') / data.get('base_width')
        self.scale_y = data.get('custom_height') / data.get('base_height')
        self.scale_uniform = min(self.scale_x, self.scale_y)
        with open(PARAMETER_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print("💾 [保存] 参数已成功保存到文件")
            print("┌" + "─" * 48 + "┐")
            print("│  ⚙️  参数更新成功                              │")
            print("├" + "─" * 48 + "┤")

            interval_str = "{:.1f}".format(data.get('interval'))
            hold_time_str = "{:.1f}".format(data.get('mouse_left_hold_time'))
            release_time_str = "{:.1f}".format(data.get('mouse_left_release_time'))
            casting_time_str = "{:.1f}".format(data.get('casting_time'))
            cycle_times_val = int(data.get('cycle_times'))
            is_overtime_val = data.get('is_overtime')
            is_auto_discard_val = data.get('is_auto_fish_discard')
            discard_level_val = data.get('discard_level')
            resolution_val = data.get('resolution')
            custom_width_val = data.get('custom_width')
            custom_height_val = data.get('custom_height')

            overtime_status = "✅" if is_overtime_val else "❌"
            overtime_text = "是" if is_overtime_val else "否"
            discard_status = "✅" if is_auto_discard_val else "❌"
            discard_text = "是" if is_auto_discard_val else "否"
            quality_name = QUALITY_LEVEL[discard_level_val - 1]

            print("│  ⏱️  循环间隔: {}s    📍 收线：{}s    📍 放线：{}s".format(
                interval_str, hold_time_str, release_time_str))
            print("│  🎣 最大拉杆：{}次     ⏳ 抛竿：{}s    {} 加时：{}".format(
                cycle_times_val, casting_time_str, overtime_status, overtime_text))
            print("│  {} 丢鱼：{}    🐟️ 丢鱼品质：{}以下品质全丢 ({}保留)".format(
                discard_status, discard_text, quality_name, quality_name))
            print("│  🖥️  分辨率：{} ({}×{})".format(
                resolution_val, custom_width_val, custom_height_val))
            print("│  📐 缩放比例：X={:.2f}  Y={:.2f}".format(self.scale_x, self.scale_y))
            print("└" + "─" * 48 + "┘")
            screen_adapt()

    def load_parameters(self):
        try:
            with open(PARAMETER_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 更新参数（线程安全）
                with self._params_lock:
                    for key, value in data.items():
                        if key in self.params:
                            self.params[key] = value

                    # 更新分辨率
                    if 'custom_width' in data:
                        self.params['custom_width'] = data['custom_width']
                        self.scale_x = self.params['custom_width'] / self.params['base_width']
                    if 'custom_height' in data:
                        self.params['custom_height'] = data['custom_height']
                        self.scale_y = self.params['custom_height'] / self.params['base_height']
                    self.scale_uniform = min(self.scale_x, self.scale_y)
                screen_init_adapt()
            return True
        except FileNotFoundError:
            print("📄 [信息] 未找到参数文件，使用默认值")
            return False
        except Exception as e:
            print("❌ [错误] 更新参数失败：{}".format(e))
            return False


# 全局配置
global_config = GlobalConfig()


def screen_init_adapt():
    from Location import location
    location.update_location()

def screen_adapt():
    from Location import location
    location.reload_base_date()
    location.update_location()

    from Action import png_template
    png_template.load_templates()

