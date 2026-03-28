from tkinter import ttk
import tkinter as tk
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
    root = ttkb.Window(themename="darkly")
    root.title("🎣 Party_Fish 自动钓鱼助手")
    root.geometry("1050x1030")
    root.minsize(900, 700)
    root.resizable(True, True)

    # 设置窗口图标
    try:
        root.iconbitmap("icon.ico")
    except:
        pass

    # ==================== 主容器 ====================
    main_paned = ttkb.Panedwindow(root, orient=HORIZONTAL)
    main_paned.pack(fill=BOTH, expand=YES, padx=12, pady=12)

    main_paned.columnconfigure(0, weight=0, minsize=300)
    main_paned.columnconfigure(1, weight=1, minsize=500)
    main_paned.rowconfigure(0, weight=1)

    # ==================== 左侧面板（设置区域 - 可滚动） ====================
    left_container = ttkb.Frame(main_paned, width=400)
    main_paned.add(left_container, weight=0)

    # 左侧滚动区域
    left_canvas = tk.Canvas(left_container, highlightthickness=0, bd=0,width=350)
    left_scrollbar = ttkb.Scrollbar(left_container, orient=VERTICAL, command=left_canvas.yview, bootstyle="rounded")
    left_scrollable = ttkb.Frame(left_canvas)

    left_scrollable.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
    left_canvas.create_window((12, 8), window=left_scrollable, anchor="nw",width=350)
    left_canvas.configure(yscrollcommand=left_scrollbar.set)

    left_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
    left_scrollbar.pack(side=RIGHT, fill=Y)

    # 鼠标滚轮支持
    def _on_mousewheel(event):
        left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    left_canvas.bind("<Enter>", lambda e: left_canvas.bind_all("<MouseWheel>", _on_mousewheel))
    left_canvas.bind("<Leave>", lambda e: left_canvas.unbind_all("<MouseWheel>"))

    # ==================== 左侧内容 ====================
    left_panel = left_scrollable

    # 标题区域
    title_frame = ttkb.Frame(left_panel)
    title_frame.pack(fill=X, pady=(0, 15))

    title_label = ttkb.Label(
        title_frame,
        text="🎣 Party_Fish",
        font=("Segoe UI", 20, "bold"),
        bootstyle="primary"
    )
    title_label.pack()

    subtitle_label = ttkb.Label(
        title_frame,
        text="自动钓鱼参数配置",
        font=("Segoe UI", 9),
        bootstyle="secondary"
    )
    subtitle_label.pack()

    # ==================== 窗口置顶控制 ====================
    window_card = ttkb.Labelframe(
        left_panel,
        text=" 🪟 窗口控制 ",
        padding=10,
        bootstyle="secondary"
    )
    window_card.pack(fill=X, pady=(0, 6))

    # 置顶状态变量
    is_topmost = tk.BooleanVar(value=False)

    def toggle_topmost():
        """切换窗口置顶状态"""
        if is_topmost.get():
            # 当前是置顶状态，点击后取消置顶
            root.attributes('-topmost', False)
            is_topmost.set(False)
            topmost_btn.config(text="📌 窗口置顶", bootstyle="secondary")
        else:
            # 当前不是置顶状态，点击后启用置顶
            root.attributes('-topmost', True)
            is_topmost.set(True)
            topmost_btn.config(text="🔝 窗口置顶", bootstyle="success")

    # 置顶按钮
    topmost_btn = ttkb.Button(
        window_card,
        text="📌 窗口置顶",
        command=toggle_topmost,
        bootstyle="secondary",
        width=20
    )
    topmost_btn.pack(pady=5)

    # 置顶提示
    ttkb.Label(
        window_card,
        text="💡 点击按钮启用置顶，再次点击取消",
        font=("Segoe UI", 8),
        bootstyle="secondary"
    ).pack(pady=(5, 0))

    # ==================== 钓鱼参数卡片 ====================
    params_card = ttkb.Labelframe(
        left_panel,
        text=" ⚙️ 钓鱼参数 ",
        padding=12,
        bootstyle="info"
    )
    params_card.pack(fill=X, pady=(0, 10))

    # 参数网格布局
    params_grid = ttkb.Frame(params_card)
    params_grid.pack(fill=X)

    # 参数配置
    params_config = [
        ("循环间隔 (秒)", "interval", global_config.params['interval']),
        ("收线时间 (秒)", "mouse_left_hold_time", global_config.params['mouse_left_hold_time']),
        ("放线时间 (秒)", "mouse_left_release_time", global_config.params['mouse_left_release_time']),
        ("最大拉杆次数", "cycle_times", global_config.params['cycle_times']),
        ("抛竿时间 (秒)", "casting_time", global_config.params["casting_time"]),
    ]

    param_vars = {}
    for i, (label_text, key, default) in enumerate(params_config):
        ttkb.Label(params_grid, text=label_text, font=("Segoe UI", 9)).grid(
            row=i, column=0, sticky=W, pady=6, padx=(0, 10)
        )
        var = ttkb.StringVar(value=str(default))
        param_vars[key] = var
        ttkb.Entry(params_grid, textvariable=var, width=12, font=("Segoe UI", 9)).grid(
            row=i, column=1, sticky=E, pady=6
        )

    params_grid.columnconfigure(0, weight=1)
    params_grid.columnconfigure(1, weight=0)

    # ==================== 加时选项卡片 ====================
    overtime_card = ttkb.Labelframe(
        left_panel,
        text=" ⏱️ 加时选项 ",
        padding=12,
        bootstyle="warning"
    )
    overtime_card.pack(fill=X, pady=(0, 10))

    overtime_var_option = ttkb.IntVar(value=global_config.params['is_overtime'])

    overtime_btn_frame = ttkb.Frame(overtime_card)
    overtime_btn_frame.pack()

    ttkb.Radiobutton(
        overtime_btn_frame,
        text="✅ 开启",
        variable=overtime_var_option,
        value=1,
        bootstyle="success-outline-toolbutton",
        width=12
    ).pack(side=LEFT, padx=10)

    ttkb.Radiobutton(
        overtime_btn_frame,
        text="❌ 关闭",
        variable=overtime_var_option,
        value=0,
        bootstyle="danger-outline-toolbutton",
        width=12
    ).pack(side=LEFT, padx=10)

    # ==================== 自动丢鱼卡片 ====================
    discard_card = ttkb.Labelframe(
        left_panel,
        text=" 🐟 自动丢鱼 ",
        padding=12,
        bootstyle="danger"
    )
    discard_card.pack(fill=X, pady=(0, 10))

    # 是否自动丢鱼
    discard_frame = ttkb.Frame(discard_card)
    discard_frame.pack(fill=X, pady=(0, 10))

    ttkb.Label(discard_frame, text="自动丢鱼", font=("Segoe UI", 9)).pack(side=LEFT)

    discard_option_var = ttkb.IntVar(value=global_config.params['is_auto_fish_discard'])

    discard_btn_frame = ttkb.Frame(discard_frame)
    discard_btn_frame.pack(side=RIGHT)

    ttkb.Radiobutton(
        discard_btn_frame,
        text="开启",
        variable=discard_option_var,
        value=1,
        bootstyle="success-outline-toolbutton",
        width=5
    ).pack(side=LEFT, padx=5)

    ttkb.Radiobutton(
        discard_btn_frame,
        text="关闭",
        variable=discard_option_var,
        value=0,
        bootstyle="danger-outline-toolbutton",
        width=5
    ).pack(side=LEFT, padx=5)

    # 丢鱼品质阈值
    def on_discard_level_select(event):
        global auto_discard_level_var
        selected = discard_level_combo.get()
        auto_discard_level_var = QUALITY_LEVEL_MAP.get(selected, 4)

    discard_level_frame = ttkb.Frame(discard_card)
    discard_level_frame.pack(fill=X)

    ttkb.Label(discard_level_frame, text="丢鱼品质阈值:", font=("Segoe UI", 9)).pack(side=LEFT)

    discard_level_combo = ttk.Combobox(
        discard_level_frame,
        values=QUALITY_LEVELS,
        state="readonly",
        width=12
    )
    discard_level_combo.set(QUALITY_LEVELS[global_config.params['discard_level'] - 1])
    discard_level_combo.bind("<<ComboboxSelected>>", on_discard_level_select)
    discard_level_combo.pack(side=RIGHT)

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

    # ==================== 保存按钮 ====================
    save_frame = ttkb.Frame(left_panel)
    save_frame.pack(fill=X, pady=(10, 5))

    def update_and_refresh():
        global auto_discard_level_var
        try:
            global_config.update(
                interval=float(param_vars['interval'].get()),
                mouse_left_hold_time=float(param_vars['mouse_left_hold_time'].get()),
                mouse_left_release_time=float(param_vars['mouse_left_release_time'].get()),
                cycle_times=float(param_vars['cycle_times'].get()),
                casting_time=float(param_vars['casting_time'].get()),
                is_overtime=overtime_var_option.get(),
                is_auto_fish_discard=discard_option_var.get(),
                discard_level=auto_discard_level_var,
                resolution=resolution_var.get(),
                custom_width=int(custom_width_var.get()),
                custom_height=int(custom_height_var.get())
            )
            resolution_info_var.set(
                f"当前: {global_config.params['custom_width']}×{global_config.params['custom_height']}")
            save_status_label.config(text="✅ 参数已保存", bootstyle="success")
            root.after(2000, lambda: save_status_label.config(text="", bootstyle="light"))
        except ValueError as e:
            save_status_label.config(text=f"❌ 输入无效: {e}", bootstyle="danger")
            root.after(3000, lambda: save_status_label.config(text="", bootstyle="light"))

    save_btn = ttkb.Button(
        save_frame,
        text="💾 保存设置",
        command=update_and_refresh,
        bootstyle="success",
        width=20
    )
    save_btn.pack(pady=5)

    # 状态提示
    save_status_label = ttkb.Label(
        save_frame,
        text="",
        font=("Segoe UI", 9),
        bootstyle="light"
    )
    save_status_label.pack()

    # ==================== 右侧面板（钓鱼记录区域） ====================
    right_panel = ttkb.Frame(main_paned)
    right_panel.grid(row=0, column=1, sticky="nsew")
    main_paned.add(right_panel, weight=1)

    # 钓鱼记录卡片
    record_card = ttkb.Labelframe(
        right_panel,
        text=" 🐟 钓鱼记录 ",
        padding=12,
        bootstyle="primary"
    )
    record_card.pack(fill=BOTH, expand=YES)

    # 工具栏
    toolbar = ttkb.Frame(record_card)
    toolbar.pack(fill=X, pady=(0, 10))

    # 视图切换
    view_mode = ttkb.StringVar(value="current")

    def set_view(mode):
        view_mode.set(mode)
        update_fish_display()

    ttkb.Button(
        toolbar,
        text="本次钓鱼",
        bootstyle="info-outline",
        width=12,
        command=lambda: set_view("current")
    ).pack(side=LEFT, padx=2)

    ttkb.Button(
        toolbar,
        text="历史总览",
        bootstyle="info-outline",
        width=12,
        command=lambda: set_view("all")
    ).pack(side=LEFT, padx=2)

    ttkb.Button(
        toolbar,
        text="🔄 刷新",
        bootstyle="info-outline",
        width=8,
        command=lambda: update_fish_display()
    ).pack(side=RIGHT, padx=2)

    # 搜索栏
    search_frame = ttkb.Frame(record_card)
    search_frame.pack(fill=X, pady=(0, 10))

    search_var = ttkb.StringVar()
    search_entry = ttkb.Entry(search_frame, textvariable=search_var, width=20, font=("Segoe UI", 9))
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

    ttkb.Button(
        search_frame,
        text="🔍 搜索",
        bootstyle="info-outline",
        width=8,
        command=lambda: update_fish_display()
    ).pack(side=LEFT, padx=2)

    # 品质筛选
    quality_var = ttkb.StringVar(value="全部")
    ttkb.Label(search_frame, text="品质:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(10, 5))

    quality_combo = ttk.Combobox(
        search_frame,
        textvariable=quality_var,
        values=["全部"] + QUALITY_LEVELS,
        width=10,
        state="readonly"
    )
    quality_combo.pack(side=LEFT)
    quality_combo.bind("<<ComboboxSelected>>", lambda e: update_fish_display())

    # 记录表格
    tree_frame = ttkb.Frame(record_card)
    tree_frame.pack(fill=BOTH, expand=YES)

    columns = ("时间", "名称", "品质", "重量")
    fish_tree = ttkb.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        height=18,
        bootstyle="info"
    )

    # 滚动条
    tree_scroll = ttkb.Scrollbar(tree_frame, orient=VERTICAL, command=fish_tree.yview, bootstyle="rounded")
    fish_tree.configure(yscrollcommand=tree_scroll.set)

    # 设置列
    fish_tree.heading("时间", text="时间")
    fish_tree.heading("名称", text="鱼名")
    fish_tree.heading("品质", text="品质")
    fish_tree.heading("重量", text="重量")

    fish_tree.column("时间", width=150, anchor="center")
    fish_tree.column("名称", width=120, anchor="w")
    fish_tree.column("品质", width=60, anchor="center")
    fish_tree.column("重量", width=80, anchor="center")

    # 品质颜色标签
    fish_tree.tag_configure("标准", background="#FFFFFF", foreground="#000000")
    fish_tree.tag_configure("非凡", background="#2ECC71", foreground="#000000")
    fish_tree.tag_configure("稀有", background="#3498DB", foreground="#FFFFFF")
    fish_tree.tag_configure("史诗", background="#9B59B6", foreground="#FFFFFF")
    fish_tree.tag_configure("传奇", background="#E67E22", foreground="#000000")

    fish_tree.pack(side=LEFT, fill=BOTH, expand=YES)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # 鼠标滚轮
    def on_tree_mousewheel(event):
        fish_tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

    fish_tree.bind("<MouseWheel>", on_tree_mousewheel)

    # 统计信息
    stats_var = ttkb.StringVar(value="共 0 条记录")
    stats_label = ttkb.Label(
        record_card,
        textvariable=stats_var,
        font=("Segoe UI", 9),
        bootstyle="info"
    )
    stats_label.pack(pady=(8, 0))

    # 更新显示函数
    def update_fish_display():
        for item in fish_tree.get_children():
            fish_tree.delete(item)

        keyword = search_var.get()
        if keyword == "搜索鱼名...":
            keyword = ""

        use_session = (view_mode.get() == "current")
        quality_filter = quality_var.get()

        filtered = search_fish_records(keyword, quality_filter, use_session)

        for record in reversed(filtered[-200:]):
            time_display = record.timestamp if record.timestamp else "未知时间"
            quality_tag = record.quality if record.quality in QUALITY_LEVELS else "标准"

            fish_tree.insert("", "end", values=(
                time_display,
                record.name,
                record.quality,
                record.weight
            ), tags=(quality_tag,))

        total = len(filtered)
        stats_var.set(f"{'本次' if use_session else '总计'}: {total} 条")

    def safe_update():
        try:
            root.after(0, update_fish_display)
        except:
            pass

    global_config.gui_fish_update_callback = safe_update
    update_fish_display()

    # ==================== 底部状态栏 ====================
    status_bar = ttkb.Frame(root)
    status_bar.pack(fill=X, side=BOTTOM, padx=10, pady=(0, 5))

    ttkb.Separator(status_bar, bootstyle="secondary").pack(fill=X, pady=(0, 5))

    status_frame = ttkb.Frame(status_bar)
    status_frame.pack(fill=X)

    ttkb.Label(
        status_frame,
        text="⌨️ 快捷键: F2 - 启动/暂停钓鱼 | F3 - 启动/暂停放生",
        font=("Segoe UI", 8),
        bootstyle="secondary"
    ).pack(side=LEFT)

    ttkb.Label(
        status_frame,
        text="v4.2 | Party_Fish",
        font=("Segoe UI", 8),
        bootstyle="secondary"
    ).pack(side=RIGHT)

    # 运行
    root.mainloop()
