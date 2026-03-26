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
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.off_x = 0
        self.off_y = 0
        self.scr = None
        self.gui_fish_update_callback = None
        self.bait_count_val = None
        self.auto_fish_thread_event = None
        self.auto_fish_discard_thread_event = None
        self.params = {
            "interval": 0.4,
            "mouse_left_hold_time": 1.8,
            "mouse_left_release_time": 0.7,
            "cycle_times": 20.0,
            "casting_time": 1.65,
            "is_overtime": 1,
            "is_auto_fish_discard": 0,
            "auto_discard_speed": 0.4,
            "discard_level": 4,
            "resolution": "2K",
            "custom_width": 2560,
            "custom_height": 1440,
            "base_width": 2560,
            "base_height": 1440
        }

        # 线程锁
        self._param_lock = threading.Lock()

    def update(self, **kwargs):
        # 批量更新参数
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value
        self.save_parameters()
        self.calculate_offset()

    def save_parameters(self):
        global QUALITY_LEVEL_MAP
        data = self.params.copy()
        self.scale_x = data.get('custom_width') / data.get('base_width')
        self.scale_y = data.get('custom_height') / data.get('base_height')
        self.calculate_offset()
        with open(PARAMETER_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print("💾 [保存] 参数已成功保存到文件")
            print("┌" + "─" * 48 + "┐")
            print("│  ⚙️  参数更新成功                              │")
            print("├" + "─" * 48 + "┤")
            print(
                f"│  ⏱️  循环间隔: {data.get('interval'):.1f}s    📍 收线: {data.get('mouse_left_hold_time'):.1f}s    📍 放线: {data.get('mouse_left_release_time'):.1f}s")
            print(
                f"│  🎣 最大拉杆: {data.get('cycle_times')}次     ⏳ 抛竿: {data.get('casting_time'):.1f}s    {'✅' if data.get('is_overtime') else '❌'} 加时: {'是' if data.get('is_overtime') else '否'}")
            print(
                f"│  {'✅' if data.get('is_auto_fish_discard') else '❌'} 丢鱼: {'是' if data.get('is_auto_fish_discard') else '否'}    🐟️ 丢鱼品质: {QUALITY_LEVEL[data.get('discard_level') - 1]}以下品质全丢({QUALITY_LEVEL[data.get('discard_level') - 1]}保留)")
            print(
                f"│  🖥️  分辨率: {data.get('resolution')} ({data.get('custom_width')}×{data.get('custom_height')})")
            print(f"│  📐 缩放比例: X={self.scale_x:.2f}  Y={self.scale_y:.2f}")
            print("└" + "─" * 48 + "┘")
            screen_adapt()

    def load_parameters(self):
        try:
            with open(PARAMETER_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 更新参数
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
                self.calculate_offset()
                screen_adapt()
            return True
        except FileNotFoundError:
            print("📄 [信息] 未找到参数文件，使用默认值")
            return False
        except Exception as e:
            print(f"❌ [错误] 更新参数失败: {e}")
            return False

    def calculate_offset(self):
        self.off_x = self.params['custom_width'] - self.params['base_width']
        self.off_y = self.params['custom_height'] - self.params['base_height']


# 全局配置
global_config = GlobalConfig()


def screen_adapt():
    from Location import location
    if global_config.scale_x == global_config.scale_y:
        if global_config.scale_x == 1.0:
            return
        location.update_location_percentage_not_change()
    else:
        location.update_location_percentage_change()
