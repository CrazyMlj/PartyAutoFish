from tkinter import ttk

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from FishRecord import search_fish_records
from GlobalConfig import global_config

## 创建 Tkinter 窗口（现代化UI设计 - 左右分栏布局）
QUALITY_LEVELS = ["标准", "非凡", "稀有", "史诗", "传奇"]
QUALITY_COLORS = {
    "标准": "⚪",
    "非凡": "🟢",
    "稀有": "🔵",
    "史诗": "🟣",
    "传奇": "🟡"
}
QUALITY_LEVEL_MAP = {
    "标准": 1,
    "非凡": 2,
    "稀有": 3,
    "史诗": 4,
    "传奇": 5
}

auto_discard_level_var = 4

def create_gui():
    # 创建现代化主题窗口
    root = ttkb.Window(themename="darkly")  # 使用深色主题
    root.title("🎣 Party_Fish 自动钓鱼助手")
    root.geometry("950x890")  # 增加高度以容纳所有内容
    root.minsize(900, 650)  # 最小尺寸
    root.resizable(True, True)  # 允许调整大小

    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap("icon.ico")
    except:
        pass

    # ==================== 主容器（固定布局，左右分栏） ====================
    main_frame = ttkb.Frame(root, padding=12)
    main_frame.pack(fill=BOTH, expand=YES)

    # 配置主框架的行列权重
    main_frame.columnconfigure(0, weight=0, minsize=300)  # 左侧固定宽度
    main_frame.columnconfigure(1, weight=1, minsize=500)  # 右侧自适应扩展
    main_frame.rowconfigure(0, weight=1)  # 内容区域自适应高度

    # ==================== 左侧面板（设置区域） ====================
    left_panel = ttkb.Frame(main_frame)
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

    # ==================== 标题区域 ====================
    title_frame = ttkb.Frame(left_panel)
    title_frame.pack(fill=X, pady=(0, 8))

    title_label = ttkb.Label(
        title_frame,
        text="🎣 Party_Fish",
        font=("Segoe UI", 16, "bold"),
        bootstyle="light"
    )
    title_label.pack()
    subtitle_label = ttkb.Label(
        title_frame,
        text="自动钓鱼参数配置",
        font=("Segoe UI", 8),
        bootstyle="light"
    )
    subtitle_label.pack()

    # ==================== 钓鱼参数卡片 ====================
    params_card = ttkb.Labelframe(
        left_panel,
        text=" ⚙️ 钓鱼参数 ",
        padding=10,
        bootstyle="info"
    )
    params_card.pack(fill=X, pady=(0, 6))

    # 参数输入样式
    def create_param_row(parent, label_text, var, row, tooltip=""):
        label = ttkb.Label(parent, text=label_text, font=("Segoe UI", 9))
        label.grid(row=row, column=0, sticky=W, pady=3, padx=(0, 8))

        entry = ttkb.Entry(parent, textvariable=var, width=10, font=("Segoe UI", 9))
        entry.grid(row=row, column=1, sticky=E, pady=3)
        return entry

    # 循环间隔
    interval_var = ttkb.StringVar(value=str(global_config.params['interval']))
    create_param_row(params_card, "循环间隔 (秒)", interval_var, 0)

    # 收线时间
    mouse_left_hold_time_var = ttkb.StringVar(value=str(global_config.params['mouse_left_hold_time']))
    create_param_row(params_card, "收线时间 (秒)", mouse_left_hold_time_var, 1)

    # 放线时间
    mouse_left_release_time_var = ttkb.StringVar(value=str(global_config.params['mouse_left_release_time']))
    create_param_row(params_card, "放线时间 (秒)", mouse_left_release_time_var, 2)

    # 最大拉线次数
    cycle_times_var = ttkb.StringVar(value=str(global_config.params['cycle_times']))
    create_param_row(params_card, "最大拉杆次数", cycle_times_var, 3)

    # 抛竿时间
    casting_time_var = ttkb.StringVar(value=str(global_config.params["casting_time"]))
    create_param_row(params_card, "抛竿时间 (秒)", casting_time_var, 4)

    # 配置列宽
    params_card.columnconfigure(0, weight=1)
    params_card.columnconfigure(1, weight=0)

    # ==================== 加时选项卡片 ====================
    overtime_card = ttkb.Labelframe(
        left_panel,
        text=" ⏱️ 加时选项 ",
        padding=10,
        bootstyle="warning"
    )

    overtime_card.pack(fill=X, pady=(0, 6))

    overtime_var_option = ttkb.IntVar(value=global_config.params['is_overtime'])

    overtime_frame = ttkb.Frame(overtime_card)
    overtime_frame.pack(fill=X)

    overtime_label = ttkb.Label(overtime_frame, text="是否自动加时", font=("Segoe UI", 9))
    overtime_label.pack(side=LEFT)

    overtime_btn_frame = ttkb.Frame(overtime_frame)
    overtime_btn_frame.pack(side=RIGHT)

    overtime_yes = ttkb.Radiobutton(
        overtime_btn_frame,
        text="是",
        variable=overtime_var_option,
        value=1,
        bootstyle="success-outline-toolbutton"
    )
    overtime_yes.pack(side=LEFT, padx=5)

    overtime_no = ttkb.Radiobutton(
        overtime_btn_frame,
        text="否",
        variable=overtime_var_option,
        value=0,
        bootstyle="danger-outline-toolbutton"
    )
    overtime_no.pack(side=LEFT, padx=5)

    # ======================= 自动丢鱼 ======================
    auto_discard_fish = ttkb.Labelframe(
        left_panel,
        text="🐟️丢鱼选项 ",
        padding=10,
        bootstyle="error"
    )
    auto_discard_fish.pack(fill=X, pady=(0, 6))

    auto_discard_fish_option_var = ttkb.IntVar(value=global_config.params['is_auto_fish_discard'])

    auto_discard_frame = ttkb.Frame(auto_discard_fish)
    auto_discard_frame.pack(fill=X)

    auto_discard_label = ttkb.Label(auto_discard_frame, text="是否自动丢鱼", font=("Segoe UI", 9))
    auto_discard_label.pack(side=LEFT)

    auto_discard_btn_frame = ttkb.Frame(auto_discard_frame)
    auto_discard_btn_frame.pack(side=RIGHT)

    auto_discard_yes = ttkb.Radiobutton(
        auto_discard_btn_frame,
        text="是",
        variable=auto_discard_fish_option_var,
        value=1,
        bootstyle="success-outline-toolbutton"
    )
    auto_discard_yes.pack(side=LEFT, padx=5)

    auto_discard_no = ttkb.Radiobutton(
        auto_discard_btn_frame,
        text="否",
        variable=auto_discard_fish_option_var,
        value=0,
        bootstyle="danger-outline-toolbutton"
    )
    auto_discard_no.pack(side=LEFT, padx=5)

    def on_select(event):
        global auto_discard_level_var
        selected = auto_discard_combo.get()
        auto_discard_level_var = QUALITY_LEVEL_MAP.get(selected)

    # 创建下拉选择框
    auto_discard_combo = ttk.Combobox(
        auto_discard_fish,
        values=QUALITY_LEVELS,
        state="readonly",  # 只读，不能手动输入
        width=20
    )
    auto_discard_combo.set(QUALITY_LEVELS[global_config.params['discard_level'] - 1])  # 默认选中
    auto_discard_combo.bind("<<ComboboxSelected>>", on_select)
    auto_discard_combo.pack(pady=10)

    # ==================== 分辨率设置卡片 ====================
    resolution_card = ttkb.Labelframe(
        left_panel,
        text=" 🖥️ 分辨率设置 ",
        padding=10,
        bootstyle="success"
    )
    resolution_card.pack(fill=X, pady=(0, 6))

    resolution_var = ttkb.StringVar(value=global_config.params['resolution'])
    custom_width_var = ttkb.StringVar(value=str(global_config.params['custom_width']))
    custom_height_var = ttkb.StringVar(value=str(global_config.params['custom_height']))

    # 分辨率选择按钮组（使用2x2网格布局）
    res_btn_frame = ttkb.Frame(resolution_card)
    res_btn_frame.pack(fill=X, pady=(0, 6))

    resolutions = [("1080P", "1080P"), ("2K", "2K"), ("4K", "4K"), ("自定义", "自定义")]

    # 自定义分辨率输入框容器
    custom_frame = ttkb.Frame(resolution_card)

    custom_width_label = ttkb.Label(custom_frame, text="宽:", font=("Segoe UI", 9))
    custom_width_label.pack(side=LEFT, padx=(0, 3))

    custom_width_entry = ttkb.Entry(custom_frame, textvariable=custom_width_var, width=6, font=("Segoe UI", 9))
    custom_width_entry.pack(side=LEFT, padx=(0, 10))

    custom_height_label = ttkb.Label(custom_frame, text="高:", font=("Segoe UI", 9))
    custom_height_label.pack(side=LEFT, padx=(0, 3))

    custom_height_entry = ttkb.Entry(custom_frame, textvariable=custom_height_var, width=6, font=("Segoe UI", 9))
    custom_height_entry.pack(side=LEFT)

    # 当前分辨率信息标签
    resolution_info_var = ttkb.StringVar(
        value=f"当前: {global_config.params['custom_width']}×{global_config.params['custom_height']}")
    info_label = ttkb.Label(
        resolution_card,
        textvariable=resolution_info_var,
        font=("Segoe UI", 8),
        bootstyle="info"
    )

    def update_resolution_info():
        res = resolution_var.get()
        if res == "1080P":
            resolution_info_var.set("当前: 1920×1080")
        elif res == "2K":
            resolution_info_var.set("当前: 2560×1440")
        elif res == "4K":
            resolution_info_var.set("当前: 3840×2160")
        else:
            resolution_info_var.set(f"当前: {custom_width_var.get()}×{custom_height_var.get()}")

    # 当分辨率选择改变时，更新自定义输入框状态
    def on_resolution_change():
        # 先隐藏所有动态元素
        custom_frame.pack_forget()
        info_label.pack_forget()

        if resolution_var.get() == "自定义":
            # 显示自定义输入框
            custom_frame.pack(fill=X, pady=(5, 0))
        else:
            # 根据选择更新显示值
            if resolution_var.get() == "1080P":
                custom_width_var.set("1920")
                custom_height_var.set("1080")
            elif resolution_var.get() == "2K":
                custom_width_var.set("2560")
                custom_height_var.set("1440")
            elif resolution_var.get() == "4K":
                custom_width_var.set("3840")
                custom_height_var.set("2160")
        # 始终显示分辨率信息标签
        info_label.pack(pady=(8, 0))
        update_resolution_info()

    # 创建分辨率选择按钮（2x2网格布局）
    res_btn_frame.columnconfigure(0, weight=1)
    res_btn_frame.columnconfigure(1, weight=1)
    for i, (text, value) in enumerate(resolutions):
        rb = ttkb.Radiobutton(
            res_btn_frame,
            text=text,
            variable=resolution_var,
            value=value,
            bootstyle="info-outline-toolbutton",
            width=9,
            command=on_resolution_change
        )
        rb.grid(row=i // 2, column=i % 2, padx=2, pady=2, sticky="ew")

    # 初始化显示状态
    if global_config.params['resolution'] == "自定义":
        custom_frame.pack(fill=X, pady=(5, 0))
    info_label.pack(pady=(8, 0))

    # ==================== 右侧面板（钓鱼记录区域） ====================
    right_panel = ttkb.Frame(main_frame)
    right_panel.grid(row=0, column=1, sticky="nsew")

    # ==================== 钓鱼记录卡片 ====================
    fish_record_card = ttkb.Labelframe(
        right_panel,
        text=" 🐟 钓鱼记录 ",
        padding=12,
        bootstyle="primary"
    )
    fish_record_card.pack(fill=BOTH, expand=YES)

    # 切换按钮（本次/总览）
    record_view_frame = ttkb.Frame(fish_record_card)
    record_view_frame.pack(fill=X, pady=(0, 10))

    view_mode = ttkb.StringVar(value="current")

    current_btn = ttkb.Radiobutton(
        record_view_frame,
        text="本次钓鱼",
        variable=view_mode,
        value="current",
        bootstyle="info-outline-toolbutton",
        command=lambda: update_fish_display()
    )
    current_btn.pack(side=LEFT, padx=5)

    all_btn = ttkb.Radiobutton(
        record_view_frame,
        text="历史总览",
        variable=view_mode,
        value="all",
        bootstyle="info-outline-toolbutton",
        command=lambda: update_fish_display()
    )
    all_btn.pack(side=LEFT, padx=5)

    # 刷新按钮
    refresh_btn = ttkb.Button(
        record_view_frame,
        text="🔄",
        command=lambda: update_fish_display(),
        bootstyle="info-outline",
        width=3
    )
    refresh_btn.pack(side=RIGHT, padx=5)

    # 搜索和筛选框
    search_frame = ttkb.Frame(fish_record_card)
    search_frame.pack(fill=X, pady=(0, 10))

    search_var = ttkb.StringVar()
    search_entry = ttkb.Entry(search_frame, textvariable=search_var, width=15, font=("Segoe UI", 9))
    search_entry.pack(side=LEFT, padx=(0, 5))
    search_entry.insert(0, "搜索鱼名...")

    def on_search_focus_in(event):
        if search_entry.get() == "搜索鱼名...":
            search_entry.delete(0, "end")

    def on_search_focus_out(event):
        if not search_entry.get():
            search_entry.insert(0, "搜索鱼名...")

    search_entry.bind("<FocusIn>", on_search_focus_in)
    search_entry.bind("<FocusOut>", on_search_focus_out)
    search_entry.bind("<Return>", lambda e: update_fish_display())

    search_btn = ttkb.Button(
        search_frame,
        text="🔍",
        command=lambda: update_fish_display(),
        bootstyle="info-outline",
        width=3
    )
    search_btn.pack(side=LEFT, padx=(0, 10))

    # 品质筛选
    quality_var = ttkb.StringVar(value="全部")
    quality_label = ttkb.Label(search_frame, text="品质:", font=("Segoe UI", 9))
    quality_label.pack(side=LEFT)
    quality_combo = ttkb.Combobox(
        search_frame,
        textvariable=quality_var,
        values=["全部"] + QUALITY_LEVELS,
        width=8,
        state="readonly",
        font=("Segoe UI", 9)
    )
    quality_combo.pack(side=LEFT, padx=5)
    quality_combo.bind("<<ComboboxSelected>>", lambda e: update_fish_display())

    # 记录列表容器（包含Treeview和滚动条）
    tree_container = ttkb.Frame(fish_record_card)
    tree_container.pack(fill=BOTH, expand=YES, pady=(0, 8))

    # 记录列表（使用Treeview）
    columns = ("时间", "名称", "品质", "重量")
    fish_tree = ttkb.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        height=15,
        bootstyle="info"
    )

    # 添加垂直滚动条（放在Treeview右侧）
    tree_scroll = ttkb.Scrollbar(tree_container, orient="vertical", command=fish_tree.yview, bootstyle="rounded")
    fish_tree.configure(yscrollcommand=tree_scroll.set)

    # 设置列标题和宽度
    fish_tree.heading("时间", text="时间")
    fish_tree.heading("名称", text="鱼名")
    fish_tree.heading("品质", text="品质")
    fish_tree.heading("重量", text="重量")

    fish_tree.column("时间", width=145, anchor="center")  # 增加宽度以显示完整日期时间(年月日时分秒)
    fish_tree.column("名称", width=110, anchor="w")
    fish_tree.column("品质", width=50, anchor="center")
    fish_tree.column("重量", width=65, anchor="center")

    # 布局Treeview和滚动条
    fish_tree.pack(side=LEFT, fill=BOTH, expand=YES)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # 配置品质颜色标签（背景色和前景色）
    # 标准-白色背景黑色字体, 非凡-绿色, 稀有-蓝色, 史诗-紫色, 传奇-橙色
    fish_tree.tag_configure("标准", background="#FFFFFF", foreground="#000000")
    fish_tree.tag_configure("非凡", background="#2ECC71", foreground="#000000")
    fish_tree.tag_configure("稀有", background="#3498DB", foreground="#FFFFFF")
    fish_tree.tag_configure("史诗", background="#9B59B6", foreground="#FFFFFF")
    fish_tree.tag_configure("传奇", background="#E67E22", foreground="#000000")

    # 绑定鼠标滚轮到Treeview
    def on_tree_mousewheel(event):
        fish_tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

    fish_tree.bind("<MouseWheel>", on_tree_mousewheel)

    # 统计信息
    stats_var = ttkb.StringVar(value="共 0 条记录")
    stats_label = ttkb.Label(
        fish_record_card,
        textvariable=stats_var,
        font=("Segoe UI", 9),
        bootstyle="info"
    )
    stats_label.pack()

    # 更新钓鱼记录显示
    def update_fish_display():
        # 清空列表
        for item in fish_tree.get_children():
            fish_tree.delete(item)

        # 获取搜索关键词
        keyword = search_var.get()
        if keyword == "搜索鱼名...":
            keyword = ""

        # 根据视图模式选择数据源
        use_session = (view_mode.get() == "current")
        quality_filter = quality_var.get()

        # 获取筛选后的记录
        filtered = search_fish_records(keyword, quality_filter, use_session)

        # 显示记录（倒序，最新的在前面）
        for record in reversed(filtered[-100:]):  # 最多显示100条
            # 直接使用完整时间戳（格式：YYYY-MM-DD HH:MM:SS）
            time_display = record.timestamp if record.timestamp else "未知时间"

            # 根据品质确定标签（用于显示颜色）
            quality_tag = record.quality if record.quality in ["标准", "非凡", "稀有", "史诗", "传奇"] else "标准"

            fish_tree.insert("", "end", values=(
                time_display,
                record.name,
                record.quality,
                record.weight
            ), tags=(quality_tag,))

        # 更新统计
        total = len(filtered)
        if use_session:
            stats_var.set(f"本次: {total} 条")
        else:
            stats_var.set(f"总计: {total} 条")

    def safe_update():
        try:
            root.after(0, update_fish_display)
        except:
            pass

    global_config.gui_fish_update_callback = safe_update

    # 初始加载
    update_fish_display()

    # ==================== 操作按钮区域（左侧面板底部） ====================
    btn_frame = ttkb.Frame(left_panel)
    btn_frame.pack(fill=X, pady=(8, 0))

    # 更新参数并刷新显示
    def update_and_refresh():
        global_config.update(
            interval=float(interval_var.get()),
            mouse_left_hold_time=float(mouse_left_hold_time_var.get()),
            mouse_left_release_time=float(mouse_left_release_time_var.get()),
            cycle_times=float(cycle_times_var.get()),
            casting_time=float(casting_time_var.get()),
            is_overtime=overtime_var_option.get(),
            is_auto_fish_discard=auto_discard_fish_option_var.get(),
            discard_level=auto_discard_level_var,
            resolution=resolution_var.get(),
            custom_width=int(custom_width_var.get()),
            custom_height=int(custom_height_var.get())
        )

        resolution_info_var.set(f"当前: {global_config.params['custom_width']}×{global_config.params['custom_height']}")
        # 显示保存成功提示
        status_label.config(text="✅ 参数已保存", bootstyle="success")
        root.after(2, lambda: status_label.config(text="按 F2 启动/暂停", bootstyle="light"))

    update_button = ttkb.Button(
        btn_frame,
        text="💾 保存设置",
        command=update_and_refresh,
        bootstyle="success",
        width=16
    )
    update_button.pack(pady=3, fill=X)

    # ==================== 状态栏（左侧面板底部） ====================
    status_frame = ttkb.Frame(left_panel)
    status_frame.pack(fill=X, pady=(8, 0))

    separator = ttkb.Separator(status_frame, bootstyle="secondary")
    separator.pack(fill=X, pady=(0, 5))

    status_label = ttkb.Label(
        status_frame,
        text="按 F2启动/暂停(钓鱼)",
        font=("Segoe UI", 9),
        bootstyle="light"
    )
    status_label.pack()

    status_label = ttkb.Label(
        status_frame,
        text="按 F3启动/暂停(放生)",
        font=("Segoe UI", 9),
        bootstyle="light"
    )
    status_label.pack()

    version_label = ttkb.Label(
        status_frame,
        text="v4.0 | Party_Fish",
        font=("Segoe UI", 7),
        bootstyle="light"
    )
    version_label.pack(pady=(2, 0))

    # 运行 GUI
    root.mainloop()
