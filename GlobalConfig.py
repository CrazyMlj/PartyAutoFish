import json
import threading

# 初始参数
interval = 0.4
mouse_left_hold_time = 1.8
mouse_left_release_time = 0.7
cycle_times = 20
casting_time = 1.65
is_overtime = 1
is_auto_fish_discard = 0
auto_discard_speed = 0.4
discard_level = 4
resolution = "2K"
custom_width = 2560
custom_height = 1440
base_width = 2560
base_height = 1440

QUALITY_LEVEL = ["标准", "非凡", "稀有", "史诗", "传奇"]
QUALITY_LEVEL_MAP = {
    "标准": 1,
    "非凡": 2,
    "稀有": 3,
    "史诗": 4,
    "传奇": 5
}

# 全局变量
scale_x = 1.0
scale_y = 1.0
scr = None
mouse = None
gui_fish_update_callback = None  # GUI更新回调（将在create_gui中设置）

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
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scr = scr
        self.gui_fish_update_callback = gui_fish_update_callback
        self.mouse = mouse
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

        # 加载保存的参数
        self.load_parameters()

    def update(self, **kwargs):
        # 批量更新参数
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value
        self.save_parameters()

    def save_parameters(self):
        global QUALITY_LEVEL_MAP, scale_x, scale_y
        data = self.params.copy()
        scale_x = self.scale_x = data.get('custom_width') / base_width
        scale_y = self.scale_y = data.get('custom_height') / base_height
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
            print(f"│  📐 缩放比例: X={scale_x:.2f}  Y={scale_y:.2f}")
            print("└" + "─" * 48 + "┘")

    def load_parameters(self):
        global scale_x, scale_y
        try:
            with open(PARAMETER_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 更新参数
                for key, value in data.items():
                    if key in self.params:
                        self.params[key] = value

                # 更新分辨率
                if "custom_width" in data:
                    self.params["custom_width"] = data["custom_width"]
                    self.scale_x = self.params["custom_width"] / self.params["base_width"]
                if "custom_height" in data:
                    self.params["custom_height"] = data["custom_height"]
                    self.scale_y = self.params["custom_height"] / self.params["base_height"]
            return True
        except FileNotFoundError:
            print("📄 [信息] 未找到参数文件，使用默认值")
            return False
        except Exception as e:
            print(f"❌ [错误] 更新参数失败: {e}")
            return False

# 全局配置
global_config = GlobalConfig()
