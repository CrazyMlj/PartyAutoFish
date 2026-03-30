import datetime
import os
import re
import threading
import time
import warnings

from Action import capture_fish_info_region
from GlobalConfig import global_config, ocr_engine, OCR_AVAILABLE

# 过滤libpng的iCCP警告（图片ICC配置文件问题）
warnings.filterwarnings("ignore", message=".*iCCP.*")
# 设置OpenCV不显示libpng警告
os.environ["OPENCV_IO_ENABLE_JASPER"] = "0"

# 品质等级定义
QUALITY_LEVELS = ["标准", "非凡", "稀有", "史诗", "传奇"]
QUALITY_COLORS = {
    "标准": "⚪",
    "非凡": "🟢",
    "稀有": "🔵",
    "史诗": "🟣",
    "传奇": "🟠"
}

# 当前会话数据
current_session_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_session_fish = []  # 当前会话钓到的鱼
all_fish_records = []  # 所有钓鱼记录（从文件加载）
fish_record_lock = threading.Lock()  # 钓鱼记录锁

# 鱼数量统计
current_quality_all_counts = {
    "标准": 0,
    "非凡": 0,
    "稀有": 0,
    "史诗": 0,
    "传奇": 0,
    "总量": 0
}
quality_all_counts = {
    "标准": 0,
    "非凡": 0,
    "稀有": 0,
    "史诗": 0,
    "传奇": 0,
    "总量": 0
}

FISH_RECORD_FILE = "./fish_records.txt"


# 单条鱼的记录
class FishRecord:

    def __init__(self, name, quality, weight):
        global current_session_id
        self.name = name if name else "未知"
        self.quality = quality if quality in QUALITY_LEVELS else "标准"
        self.weight = weight if weight else "0"
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session_id = current_session_id

    def to_dict(self):
        return {
            "name": self.name,
            "quality": self.quality,
            "weight": self.weight,
            "timestamp": self.timestamp,
            "session_id": self.session_id
        }

    def to_line(self):
        """转换为文件存储格式"""
        return f"{self.session_id}|{self.timestamp}|{self.name}|{self.quality}|{self.weight}\n"

    @staticmethod
    def from_line(line):
        """从文件行解析"""
        try:
            parts = line.strip().split("|")
            if len(parts) >= 5:
                record = FishRecord.__new__(FishRecord)
                record.session_id = parts[0]
                record.timestamp = parts[1]
                record.name = parts[2]
                record.quality = parts[3]
                record.weight = parts[4]
                return record
        except:
            pass
        return None


# 开始新的钓鱼会话
def start_new_session():
    print("🎣 [会话] 新钓鱼会话开始: {}".format(current_session_id))


# 结束当前钓鱼会话
def end_current_session():
    global current_session_id, current_session_fish
    if current_session_fish:
        print("📊 [会话] 本次钓鱼结束，共钓到 {} 条鱼".format(len(current_session_fish)))
        # 统计品质
        quality_count = {}
        for fish in current_session_fish:
            quality_count[fish.quality] = quality_count.get(fish.quality, 0) + 1
        for q, count in quality_count.items():
            emoji = QUALITY_COLORS.get(q, "⚪")
            print("   {} {}: {} 条".format(emoji, q, count))


# 使用OCR识别鱼的信息
def recognize_fish_info_ocr(img):
    if not OCR_AVAILABLE or ocr_engine is None:
        return None, None, None

    if img is None:
        return None, None, None

    try:
        # 执行OCR识别
        result, elapse = ocr_engine(img)

        if result is None or len(result) == 0:
            return None, None, None

        # 合并所有识别到的文本
        full_text = ""
        for line in result:
            if len(line) >= 2:
                full_text += line[1] + " "

        full_text = full_text.strip()

        if not full_text:
            return None, None, None

        # 解析鱼的信息
        fish_name = None
        fish_quality = None
        fish_weight = None

        # 识别品质
        for quality in QUALITY_LEVELS:
            if quality in full_text:
                fish_quality = quality
                break

        # 识别重量（匹配数字+kg或g的模式）
        weight_pattern = r'(\d+\.?\d*)\s*(kg|g|千克|克)?'
        weight_matches = re.findall(weight_pattern, full_text, re.IGNORECASE)
        if weight_matches:
            # 取最后一个匹配的数字作为重量
            for match in weight_matches:
                if match[0]:
                    fish_weight = match[0]
                    unit = match[1].lower() if match[1] else "kg"
                    if unit in ['g', '克']:
                        fish_weight = str(float(fish_weight) / 1000)
                    fish_weight = f"{float(fish_weight):.2f}kg"

        # 识别鱼名 - 优先匹配"你钓到了XXX"或"首次捕获XXX"格式
        # 使用正则表达式提取鱼名
        fish_name_patterns = [
            r'你钓到了\s*[「【\[]?\s*(.+?)\s*[」】\]]?\s*(?:标准|非凡|稀有|史诗|传说|$)',  # 你钓到了XXX
            r'首次捕获\s*[「【\[]?\s*(.+?)\s*[」】\]]?\s*(?:标准|非凡|稀有|史诗|传说|$)',  # 首次捕获XXX
            r'钓到了\s*[「【\[]?\s*(.+?)\s*[」】\]]?\s*(?:标准|非凡|稀有|史诗|传说|$)',  # 钓到了XXX
            r'捕获\s*[「【\[]?\s*(.+?)\s*[」】\]]?\s*(?:标准|非凡|稀有|史诗|传说|$)',  # 捕获XXX
        ]

        for pattern in fish_name_patterns:
            match = re.search(pattern, full_text)
            if match:
                extracted_name = match.group(1).strip()
                # 清理鱼名中的数字、单位和特殊字符
                extracted_name = re.sub(r'\d+\.?\d*\s*(kg|g|千克|克)?', '', extracted_name, flags=re.IGNORECASE)
                extracted_name = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\s]', '', extracted_name)
                extracted_name = extracted_name.strip()
                if extracted_name and len(extracted_name) >= 2:
                    fish_name = extracted_name
                    break

        # 如果上述模式都没匹配到，尝试备用方案
        if not fish_name:
            name_text = full_text
            # 移除常见前缀
            prefixes_to_remove = ['你钓到了', '首次捕获', '钓到了', '捕获', '你钓到', '钓到']
            for prefix in prefixes_to_remove:
                name_text = name_text.replace(prefix, ' ')
            # 移除品质词
            if fish_quality:
                name_text = name_text.replace(fish_quality, ' ')
            # 移除数字和单位
            name_text = re.sub(r'\d+\.?\d*\s*(kg|g|千克|克)?', '', name_text, flags=re.IGNORECASE)
            # 清理特殊字符，保留中文和英文
            name_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z]', ' ', name_text)
            # 取最长的连续中文词作为鱼名
            chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', name_text)
            if chinese_words:
                # 选择最长的词作为鱼名
                fish_name = max(chinese_words, key=len)

        return fish_name, fish_quality, fish_weight

    except Exception as e:
        print(f"❌ [错误] OCR识别失败: {e}")
        return None, None, None


# 识别并记录钓到的鱼
def record_caught_fish():
    global current_session_fish, all_fish_records

    if not OCR_AVAILABLE:
        return None

    # 等待鱼信息显示
    time.sleep(0.3)

    # 截取鱼信息区域
    img = capture_fish_info_region()
    if img is None:
        return None

    # OCR识别
    fish_name, fish_quality, fish_weight = recognize_fish_info_ocr(img)

    if fish_name is None and fish_quality is None and fish_weight is None:
        return None

    # 创建记录
    with fish_record_lock:
        fish = FishRecord(fish_name, fish_quality, fish_weight)
        current_session_fish.append(fish)
        all_fish_records.append(fish)
        update_all_quality_counts(fish)
        update_current_quality_counts(fish)
        save_fish_record(fish)

    # 终端输出
    quality_emoji = QUALITY_COLORS.get(fish.quality, "⚪")
    print("🐟 [钓到] {} {} | 品质: {} | 重量: {}".format(quality_emoji, fish_name, fish_quality, fish_weight))

    # 通知GUI更新
    if global_config.gui_fish_update_callback:
        try:
            global_config.gui_fish_update_callback()
        except:
            pass

    return fish


# 获取当前会话的钓鱼记录
def get_session_fish_list():
    with fish_record_lock:
        return list(current_session_fish)


# 获取所有钓鱼记录
def get_all_fish_list():
    with fish_record_lock:
        return list(all_fish_records)


# 搜索钓鱼记录
def search_fish_records(keyword="", quality_filter="全部", use_session=True):
    with fish_record_lock:
        records = current_session_fish if use_session else all_fish_records

        filtered = []
        for record in records:
            # 品质筛选
            if quality_filter != "全部" and record.quality != quality_filter:
                continue
            # 关键词搜索
            if keyword and keyword.lower() not in record.name.lower():
                continue
            filtered.append(record)
        return filtered


# 保存单条钓鱼记录到文件
def save_fish_record(fish_record):
    try:
        with open(FISH_RECORD_FILE, "a", encoding="utf-8") as f:
            f.write(fish_record.to_line())
    except Exception as e:
        print("❌ [错误] 保存钓鱼记录失败: {}".format(e))


# 加载所有历史钓鱼记录
def load_all_fish_records():
    global all_fish_records
    all_fish_records = []
    try:
        if os.path.exists(FISH_RECORD_FILE):
            with open(FISH_RECORD_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        record = FishRecord.from_line(line)
                        if record:
                            update_all_quality_counts(record)
                            all_fish_records.append(record)
            print("📊 [信息] 已加载 {} 条历史钓鱼记录".format(len(all_fish_records)))
    except Exception as e:
        print("❌ [错误] 加载钓鱼记录失败: {}".format(e))


# 更新概率统计
def update_all_quality_counts(fish_record):
    global quality_all_counts
    quality_all_counts[fish_record.quality] += 1
    quality_all_counts['总量'] += 1


def update_current_quality_counts(fish_record):
    global current_quality_all_counts
    current_quality_all_counts[fish_record.quality] += 1
    current_quality_all_counts['总量'] += 1


def clear_current_fish_records():
    global current_session_fish, current_quality_all_counts
    for current_quality_all_count in current_quality_all_counts:
        current_quality_all_counts[current_quality_all_count] = 0
    current_session_fish.clear()


# 清空记录
def clear_all_fish_records():
    global all_fish_records, quality_all_counts
    with fish_record_lock:
        all_fish_records.clear()
        for quality_all_count in quality_all_counts:
            quality_all_counts[quality_all_count] = 0
        # 清空记录文件
        try:
            with open(FISH_RECORD_FILE, "w", encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print("❌ [错误] 清空记录文件失败: {}".format(e))

    if global_config.gui_fish_update_callback:
        try:
            global_config.gui_fish_update_callback()
        except:
            pass
