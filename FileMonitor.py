# -*- coding: utf-8 -*-
import os
import sys
import datetime
import subprocess
import ctypes
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# 解决双击运行时工作目录为 system32 或临时目录的问题
if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

# ================== 支持语言 ==================
LANGUAGES = [("zh", "中文（简体）"), ("zh-TW", "中文（繁體）"), ("en", "English")]

# ================== 多语言翻译表 ==================
STRINGS = {
    "zh": {
        "title": "文件监控程序 - 自动关机版",
        "notebook_options": "选项",
        "notebook_help": "帮助",
        "help_title": "关于本软件",
        "help_name": "文件监控程序 (自动关机版)",
        "help_version": "版本: 1.0",
        "help_desc": "监视指定文件（或文件夹）是否出现，可自动记录日志并在检测到后执行关机。",
        "help_usage": "使用方法:\n1. 在“选项”中设置要监控的路径（文件或文件夹）。\n2. 设置检查间隔与关机延迟。\n3. 点击“开始监控”，程序将循环检测。\n4. 检测到目标后将根据设置记录日志或执行关机。",
        "copyright": "版权所有 © Dalict 2026",
        "file_label": "监控目标：",
        "browse_button": "...",
        "browse_title": "选择路径",
        "interval_label": "监控间隔（秒）：",
        "delay_label": "关机延迟（秒，0=立即关机）：",
        "enable_shutdown": "启用自动关机",
        "enable_log": "记录日志文件",
        "language_label": "界面语言：",
        "start_button": "开始监控",
        "stop_button": "停止监控",
        "monitoring_started": "开始监控: {}，间隔 {} 秒",
        "monitoring_stopped": "监控已停止",
        "check_not_found": "已执行了一次检查，目前目标还没有出现，检查继续...",
        "target_detected": "检测到目标: {}",
        "target_detected_title": "目标已检测到",
        "log_entry_time": "检测时间: ",
        "log_target_path": "检测到的目标: ",
        "log_dir": "所在目录: ",
        "log_shutdown_status": "自动关机功能状态:",
        "shutdown_enabled_delay": "  已启用，等待 {} 秒后关机",
        "shutdown_enabled_immediate": "  已启用，立即关机",
        "shutdown_disabled": "  已禁用",
        "shutdown_immediate": "正在执行立即关机...",
        "shutdown_cmd_sent": "关机命令已发送，系统即将关机",
        "shutdown_failed": "关机失败: {}",
        "cancel_shutdown": "取消关机",
        "countdown_title": "关机倒计时",
        "countdown_info": "目标已检测到: {}\n系统将在以下时间后关机：",
        "countdown_remaining": "{} 秒",
        "countdown_cancelled": "用户取消了自动关机",
        "msg_cancelled": "自动关机已取消。",
        "msg_found_no_shutdown": "目标已检测到: {}\n自动关机功能未启用。",
        "msg_found_log_disabled": "（日志记录已关闭）",
        "msg_shutdown_info": "系统即将关机...",
        "warning_no_path": "请输入或选择要监控的路径",
        "error": "错误",
        "log_divider": "========================================",
        "monitoring_log_prefix": "文件监控日志_",
        "lang_switched": "语言已切换",
        "startup_hint": "请选择路径并写出文件名开始检测吧~",
        "invalid_interval": "监控间隔设置无效，已重置为 3 秒",
        "invalid_delay": "关机延迟设置无效，已重置为 5 秒",
    },
    "zh-TW": {
        "title": "檔案監控程式 - 自動關機版",
        "notebook_options": "選項",
        "notebook_help": "說明",
        "help_title": "關於本軟體",
        "help_name": "檔案監控程式 (自動關機版)",
        "help_version": "版本: 1.0",
        "help_desc": "監視指定的檔案（或資料夾）是否出現，可自動記錄日誌並在偵測到後執行關機。",
        "help_usage": "使用方法:\n1. 在「選項」中設定要監控的路徑（檔案或資料夾）。\n2. 設定檢查間隔與關機延遲。\n3. 點選「開始監控」，程式將循環偵測。\n4. 偵測到目標後將根據設定記錄日誌或執行關機。",
        "copyright": "版權所有 © Dalict 2026",
        "file_label": "監控目標：",
        "browse_button": "...",
        "browse_title": "選擇路徑",
        "interval_label": "監控間隔（秒）：",
        "delay_label": "關機延遲（秒，0=立即關機）：",
        "enable_shutdown": "啟用自動關機",
        "enable_log": "記錄日誌檔案",
        "language_label": "介面語言：",
        "start_button": "開始監控",
        "stop_button": "停止監控",
        "monitoring_started": "開始監控: {}，間隔 {} 秒",
        "monitoring_stopped": "監控已停止",
        "check_not_found": "已執行了一次檢查，目前目標還沒有出現，檢查繼續...",
        "target_detected": "偵測到目標: {}",
        "target_detected_title": "目標已偵測到",
        "log_entry_time": "偵測時間: ",
        "log_target_path": "偵測到的目標: ",
        "log_dir": "所在目錄: ",
        "log_shutdown_status": "自動關機功能狀態:",
        "shutdown_enabled_delay": "  已啟用，等待 {} 秒後關機",
        "shutdown_enabled_immediate": "  已啟用，立即關機",
        "shutdown_disabled": "  已停用",
        "shutdown_immediate": "正在執行立即關機...",
        "shutdown_cmd_sent": "關機命令已傳送，系統即將關機",
        "shutdown_failed": "關機失敗: {}",
        "cancel_shutdown": "取消關機",
        "countdown_title": "關機倒數計時",
        "countdown_info": "目標已偵測到: {}\n系統將在以下時間後關機：",
        "countdown_remaining": "{} 秒",
        "countdown_cancelled": "使用者取消了自動關機",
        "msg_cancelled": "自動關機已取消。",
        "msg_found_no_shutdown": "目標已偵測到: {}\n自動關機功能未啟用。",
        "msg_found_log_disabled": "（日誌記錄已關閉）",
        "msg_shutdown_info": "系統即將關機...",
        "warning_no_path": "請輸入或選擇要監控的路徑",
        "error": "錯誤",
        "log_divider": "========================================",
        "monitoring_log_prefix": "檔案監控日誌_",
        "lang_switched": "語言已切換",
        "startup_hint": "請選擇路徑並寫出檔案名稱開始偵測吧~",
        "invalid_interval": "監控間隔設定無效，已重設為 3 秒",
        "invalid_delay": "關機延遲設定無效，已重設為 5 秒",
    },
    "en": {
        "title": "File Monitor - Auto Shutdown",
        "notebook_options": "Options",
        "notebook_help": "Help",
        "help_title": "About",
        "help_name": "File Monitor (Auto Shutdown)",
        "help_version": "Version: 1.0",
        "help_desc": "Monitors a specified file or folder, logs its appearance, and optionally shuts down the system.",
        "help_usage": "Usage:\n1. Set the target path (file or folder) in \"Options\".\n2. Set check interval and shutdown delay.\n3. Click \"Start Monitoring\" to begin.\n4. When the target is detected, a log is written and shutdown is executed if enabled.",
        "copyright": "Copyright © Dalict 2026",
        "file_label": "Target:",
        "browse_button": "...",
        "browse_title": "Select Path",
        "interval_label": "Check interval (sec):",
        "delay_label": "Shutdown delay (sec, 0=immediate):",
        "enable_shutdown": "Enable auto shutdown",
        "enable_log": "Save log file",
        "language_label": "Language:",
        "start_button": "Start Monitoring",
        "stop_button": "Stop Monitoring",
        "monitoring_started": "Started monitoring: {}, interval {} sec",
        "monitoring_stopped": "Monitoring stopped",
        "check_not_found": "Checked once, target not yet appeared. Monitoring continues…",
        "target_detected": "Target detected: {}",
        "target_detected_title": "Target Detected",
        "log_entry_time": "Detection time: ",
        "log_target_path": "Detected target: ",
        "log_dir": "Directory: ",
        "log_shutdown_status": "Auto shutdown status:",
        "shutdown_enabled_delay": "  Enabled, shutdown after {} sec",
        "shutdown_enabled_immediate": "  Enabled, immediate shutdown",
        "shutdown_disabled": "  Disabled",
        "shutdown_immediate": "Executing immediate shutdown...",
        "shutdown_cmd_sent": "Shutdown command sent, system will shut down",
        "shutdown_failed": "Shutdown failed: {}",
        "cancel_shutdown": "Cancel Shutdown",
        "countdown_title": "Shutdown Countdown",
        "countdown_info": "Target detected: {}\nSystem will shut down after:",
        "countdown_remaining": "{} sec",
        "countdown_cancelled": "User cancelled auto shutdown",
        "msg_cancelled": "Auto shutdown has been cancelled.",
        "msg_found_no_shutdown": "Target detected: {}\nAuto shutdown is disabled.",
        "msg_found_log_disabled": "(log disabled)",
        "msg_shutdown_info": "System is shutting down...",
        "warning_no_path": "Please enter or select a path to monitor",
        "error": "Error",
        "log_divider": "========================================",
        "monitoring_log_prefix": "file_monitor_log_",
        "lang_switched": "Language switched",
        "startup_hint": "Please select a path and enter the file name to start monitoring~",
        "invalid_interval": "Invalid check interval, reset to 3 sec",
        "invalid_delay": "Invalid shutdown delay, reset to 5 sec",
    }
}

# ================== 主应用程序类 ==================
class FileMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Monitor")
        self.root.resizable(True, True)
        self.root.minsize(620, 460)

        try:
            icon_path = self.get_icon_path()
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass

        self.lang_map = {code: name for code, name in LANGUAGES}
        self.lang = self._detect_system_lang()
        self.strings = STRINGS[self.lang]

        self.monitoring = False
        self.after_id = None
        self.target_detected = False

        self._create_widgets()
        self._apply_language()

    def get_icon_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, "ico.ico")
        return "ico.ico"

    def _detect_system_lang(self):
        """返回 'zh' / 'zh-TW' / 'en'"""
        try:
            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            if lang_id == 0x0804:          # 简体中文
                return "zh"
            elif lang_id == 0x0404:        # 繁体中文
                return "zh-TW"
            else:
                return "en"
        except:
            return "en"

    def _safe_get_int(self, tk_var, default, error_key, min_val=None, max_val=None):
        try:
            value = int(tk_var.get())
        except:
            self.log(self.strings[error_key])
            tk_var.set(default)
            return default
        if min_val is not None and value < min_val:
            self.log(self.strings[error_key])
            tk_var.set(default)
            return default
        if max_val is not None and value > max_val:
            self.log(self.strings[error_key])
            tk_var.set(default)
            return default
        return value

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_options = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_options, text="Options")
        self.frame_options.grid_columnconfigure(0, weight=0)
        self.frame_options.grid_columnconfigure(1, weight=1)
        self.frame_options.grid_columnconfigure(2, weight=0)
        self.frame_options.grid_rowconfigure(7, weight=1)

        self.lbl_file = ttk.Label(self.frame_options)
        self.lbl_file.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.file_path = tk.StringVar(value=os.path.join(os.getcwd(), ""))
        self.entry_file = ttk.Entry(self.frame_options, textvariable=self.file_path)
        self.entry_file.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.btn_browse = ttk.Button(self.frame_options, text="...", command=self.browse_folder, width=3)
        self.btn_browse.grid(row=0, column=2, padx=2, pady=5)

        self.lbl_interval = ttk.Label(self.frame_options)
        self.lbl_interval.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.interval = tk.IntVar(value=3)
        self.spin_interval = ttk.Spinbox(self.frame_options, from_=1, to=3600, textvariable=self.interval, width=10)
        self.spin_interval.grid(row=1, column=1, sticky="w", padx=5)

        self.lbl_delay = ttk.Label(self.frame_options)
        self.lbl_delay.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.shutdown_delay = tk.IntVar(value=5)
        self.entry_delay = ttk.Entry(self.frame_options, textvariable=self.shutdown_delay, width=10)
        self.entry_delay.grid(row=2, column=1, sticky="w", padx=5)

        self.enable_shutdown = tk.BooleanVar(value=True)
        self.chk_shutdown = ttk.Checkbutton(self.frame_options, variable=self.enable_shutdown)
        self.chk_shutdown.grid(row=3, column=1, sticky="w", padx=5)

        self.enable_log = tk.BooleanVar(value=True)
        self.chk_log = ttk.Checkbutton(self.frame_options, variable=self.enable_log)
        self.chk_log.grid(row=4, column=1, sticky="w", padx=5)

        self.lbl_lang = ttk.Label(self.frame_options)
        self.lbl_lang.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        lang_names = [name for code, name in LANGUAGES]
        self.combo_lang = ttk.Combobox(self.frame_options, values=lang_names, state="readonly", width=18)
        self.combo_lang.grid(row=5, column=1, sticky="w", padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_lang_change)
        self.combo_lang.set(self.lang_map[self.lang])

        self.btn_start = ttk.Button(self.frame_options, text="Start Monitoring", command=self.start_monitoring, width=15)
        self.btn_start.grid(row=6, column=1, sticky="w", padx=5, pady=10)
        self.btn_stop = ttk.Button(self.frame_options, text="Stop Monitoring", command=self.stop_monitoring, width=15, state="disabled")
        self.btn_stop.grid(row=6, column=2, sticky="w", padx=5, pady=10)

        self.status_text = tk.Text(self.frame_options, height=12, width=70, state="disabled", bg="white", wrap="word")
        self.status_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.frame_help = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_help, text="Help")
        self.help_widgets = []
        for key in ["help_title", "help_name", "help_version", "help_desc", "help_usage"]:
            if key == "help_title":
                lbl = ttk.Label(self.frame_help, font=("Arial", 12, "bold"))
                lbl.pack(pady=5)
            elif key == "help_usage":
                lbl = ttk.Label(self.frame_help, justify="left")
                lbl.pack(pady=5, padx=10, anchor="w")
            else:
                lbl = ttk.Label(self.frame_help)
                lbl.pack(pady=2, padx=10, anchor="w")
            self.help_widgets.append((key, lbl))
        self.lbl_copyright = ttk.Label(self.frame_help, text="", font=("Arial", 8))
        self.lbl_copyright.pack(side="bottom", anchor="sw", padx=10, pady=5)
        self.help_widgets.append(("copyright", self.lbl_copyright))

        self.log(self.strings["startup_hint"], no_time=True)

    def _apply_language(self):
        s = self.strings
        self.root.title(s["title"])
        self.notebook.tab(0, text=s["notebook_options"])
        self.notebook.tab(1, text=s["notebook_help"])

        self.lbl_file.config(text=s["file_label"])
        self.btn_browse.config(text=s["browse_button"])
        self.lbl_interval.config(text=s["interval_label"])
        self.lbl_delay.config(text=s["delay_label"])
        self.chk_shutdown.config(text=s["enable_shutdown"])
        self.chk_log.config(text=s["enable_log"])
        self.lbl_lang.config(text=s["language_label"])
        self.btn_start.config(text=s["start_button"])
        self.btn_stop.config(text=s["stop_button"])

        for key, lbl in self.help_widgets:
            lbl.config(text=s.get(key, ""))

    def on_lang_change(self, event=None):
        selected_name = self.combo_lang.get()
        for code, name in LANGUAGES:
            if name == selected_name:
                self.lang = code
                break
        self.strings = STRINGS[self.lang]
        self._apply_language()
        self.log(self.strings["lang_switched"], no_time=True)

    def log(self, msg, no_time=False):
        self.status_text.config(state="normal")
        if not no_time:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            self.status_text.insert(tk.END, "[{}] {}\n".format(now, msg))
        else:
            self.status_text.insert(tk.END, "{}\n".format(msg))
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")

    def browse_folder(self):
        directory = filedialog.askdirectory(
            title=self.strings["browse_title"],
            initialdir=os.getcwd()
        )
        if directory:
            if not directory.endswith(os.sep):
                directory += os.sep
            self.file_path.set(directory)

    def start_monitoring(self):
        target = self.file_path.get().strip()
        if not target:
            messagebox.showwarning("Warning", self.strings["warning_no_path"])
            return

        interval = self._safe_get_int(self.interval, 3, "invalid_interval", min_val=1, max_val=3600)
        self.entry_file.config(state="disabled")
        self.spin_interval.config(state="disabled")
        self.entry_delay.config(state="disabled")
        self.chk_shutdown.config(state="disabled")
        self.chk_log.config(state="disabled")
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")

        self.monitoring = True
        self.target_detected = False
        self.log(self.strings["monitoring_started"].format(target, interval))
        self.schedule_check()

    def stop_monitoring(self):
        self.monitoring = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.entry_file.config(state="normal")
        self.spin_interval.config(state="normal")
        self.entry_delay.config(state="normal")
        self.chk_shutdown.config(state="normal")
        self.chk_log.config(state="normal")
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.log(self.strings["monitoring_stopped"])

    def schedule_check(self):
        if not self.monitoring:
            return
        interval = self._safe_get_int(self.interval, 3, "invalid_interval", min_val=1, max_val=3600)
        self.check_file()
        self.after_id = self.root.after(interval * 1000, self.schedule_check)

    def check_file(self):
        target = self.file_path.get().strip()
        if not target:
            self.stop_monitoring()
            return
        if os.path.exists(target):
            if not self.target_detected:
                self.target_detected = True
                self.monitoring = False
                if self.after_id:
                    self.root.after_cancel(self.after_id)
                    self.after_id = None
                if self.enable_log.get():
                    self.write_log(target)
                self.log(self.strings["target_detected"].format(target))
                if self.enable_shutdown.get():
                    delay = self._safe_get_int(self.shutdown_delay, 5, "invalid_delay", min_val=0)
                    if delay == 0:
                        self.do_shutdown_immediate()
                    else:
                        self.start_countdown(delay, target)
                else:
                    self.show_found_message(target)
        else:
            self.log(self.strings["check_not_found"])

    def write_log(self, target):
        now = datetime.datetime.now()
        prefix = self.strings["monitoring_log_prefix"]
        log_name = "{}{}.log".format(prefix, now.strftime('%Y%m%d'))
        with open(log_name, "a", encoding="utf-8") as f:
            s = self.strings
            f.write(s["log_divider"] + "\n")
            f.write(s["log_entry_time"] + now.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write(s["log_target_path"] + target + "\n")
            f.write(s["log_dir"] + (os.path.dirname(target) or os.getcwd()) + "\n")
            f.write(s["log_shutdown_status"] + "\n")
            delay = self._safe_get_int(self.shutdown_delay, 5, "invalid_delay", min_val=0)
            if self.enable_shutdown.get():
                if delay > 0:
                    f.write(s["shutdown_enabled_delay"].format(delay) + "\n")
                else:
                    f.write(s["shutdown_enabled_immediate"] + "\n")
            else:
                f.write(s["shutdown_disabled"] + "\n")
            f.write(s["log_divider"] + "\n\n")

    def do_shutdown_immediate(self):
        self.log(self.strings["shutdown_immediate"])
        try:
            subprocess.Popen(['shutdown', '/s', '/t', '0'])
            self.log(self.strings["shutdown_cmd_sent"])
        except Exception as e:
            err_msg = self.strings["shutdown_failed"].format(e)
            self.log(err_msg)
            messagebox.showerror(self.strings["error"], err_msg)
        messagebox.showinfo(self.strings["msg_shutdown_info"], self.strings["msg_shutdown_info"])
        self.root.destroy()

    def start_countdown(self, delay, target):
        s = self.strings
        cw = tk.Toplevel(self.root)
        cw.title(s["countdown_title"])
        cw.resizable(False, False)
        cw.grab_set()
        try:
            icon_path = self.get_icon_path()
            if os.path.exists(icon_path):
                cw.iconbitmap(icon_path)
        except:
            pass

        remaining = tk.IntVar(value=delay)
        cancel_flag = [False]

        ttk.Label(cw, text=s["countdown_info"].format(target)).pack(padx=20, pady=10)
        counter_label = ttk.Label(cw, font=("Arial", 20))
        counter_label.pack(pady=10)

        def update_countdown():
            if cancel_flag[0]:
                cw.destroy()
                return
            cur = remaining.get()
            if cur <= 0:
                cw.destroy()
                self.execute_shutdown()
                return
            counter_label.config(text=s["countdown_remaining"].format(cur))
            remaining.set(cur - 1)
            cw.after(1000, update_countdown)

        def cancel_action():
            cancel_flag[0] = True
            self.log(s["countdown_cancelled"])
            messagebox.showinfo(s["cancel_shutdown"], s["msg_cancelled"])
            cw.destroy()
            self.stop_monitoring()

        ttk.Button(cw, text=s["cancel_shutdown"], command=cancel_action, width=15).pack(pady=10)
        cw.protocol("WM_DELETE_WINDOW", cancel_action)
        update_countdown()

    def execute_shutdown(self, *args):
        try:
            subprocess.Popen(['shutdown', '/s', '/t', '0'])
            self.log(self.strings["shutdown_cmd_sent"])
        except Exception as e:
            self.log(self.strings["shutdown_failed"].format(e))
            messagebox.showerror(self.strings["error"], self.strings["shutdown_failed"].format(e))
        messagebox.showinfo(self.strings["msg_shutdown_info"], self.strings["msg_shutdown_info"])
        self.root.destroy()

    def show_found_message(self, target):
        title = self.strings["target_detected_title"]
        msg = self.strings["msg_found_no_shutdown"].format(target)
        if not self.enable_log.get():
            msg += "\n" + self.strings["msg_found_log_disabled"]
        messagebox.showinfo(title, msg)
        self.stop_monitoring()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMonitorApp(root)
    root.mainloop()