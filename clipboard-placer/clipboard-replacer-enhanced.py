import pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import threading
import time

class ClipboardReplacer:
    def __init__(self, root):
        self.root = root
        self.root.title("剪贴板文本替换工具")
        self.root.geometry("360x360")
        self.root.resizable(False, False)
        
        # 默认替换设置
        self.default_settings = {
            "replacements": [{"from": "hduser", "to": "hduse"}],
            "auto_mode": False,
            "polling_interval": 0.5  # 检测间隔，单位秒
        }
        self.settings_file = "replacer_settings.json"
        self.settings = self.load_settings()
        
        # 剪贴板监控变量
        self.last_clipboard_content = ""
        self.monitoring_thread = None
        self.stop_monitoring = False
        
        self.create_widgets()
        
        # 启动时如果自动模式开启，则开始监控
        if self.settings["auto_mode"]:
            self.start_monitoring()
    
    def load_settings(self):
        """加载设置，如果文件不存在则创建默认设置"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # 确保新添加的设置项存在
                    if "auto_mode" not in settings:
                        settings["auto_mode"] = self.default_settings["auto_mode"]
                    if "polling_interval" not in settings:
                        settings["polling_interval"] = self.default_settings["polling_interval"]
                    return settings
            except:
                return self.default_settings
        else:
            self.save_settings(self.default_settings)
            return self.default_settings
    
    def save_settings(self, settings):
        """保存设置到文件"""
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        """创建GUI组件"""
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 创建设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="设置", menu=settings_menu)
        settings_menu.add_command(label="添加替换规则", command=self.add_replacement)
        settings_menu.add_command(label="编辑替换规则", command=self.edit_replacements)
        settings_menu.add_command(label="自动模式设置", command=self.auto_mode_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="恢复默认设置", command=self.reset_settings)
        
        # 添加说明标签
        self.instruction = tk.Label(self.root, text="点击按钮将自动替换剪贴板中的文本", wraplength=300)
        self.instruction.pack(pady=10)
        
        # 自动模式开关
        self.auto_frame = tk.Frame(self.root)
        self.auto_frame.pack(pady=5)
        
        self.auto_var = tk.BooleanVar(value=self.settings["auto_mode"])
        self.auto_check = tk.Checkbutton(self.auto_frame, text="自动检测模式", 
                                         variable=self.auto_var, command=self.toggle_auto_mode)
        self.auto_check.pack(side=tk.LEFT)
        
        self.auto_status = tk.Label(self.auto_frame, text="", fg="green")
        self.auto_status.pack(side=tk.LEFT, padx=5)
        self.update_auto_status()
        
        # 创建替换按钮
        self.replace_button = tk.Button(self.root, text="执行替换", command=self.replace_text, height=2, width=15)
        self.replace_button.pack(pady=10)
        
        # 创建状态标签
        self.status_label = tk.Label(self.root, text="准备就绪")
        self.status_label.pack(pady=5)
        
        # 创建替换规则列表框
        self.rules_frame = tk.Frame(self.root)
        self.rules_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.rules_label = tk.Label(self.rules_frame, text="当前替换规则:")
        self.rules_label.pack(anchor=tk.W, padx=20)
        
        self.rules_listbox = tk.Listbox(self.rules_frame, width=40, height=8)
        self.rules_listbox.pack(padx=20, fill=tk.BOTH, expand=True)
        
        # 更新替换规则列表显示
        self.update_rules_listbox()
        
        # 添加关闭事件处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def update_auto_status(self):
        """更新自动模式状态显示"""
        if self.settings["auto_mode"]:
            self.auto_status.config(text="已开启", fg="green")
        else:
            self.auto_status.config(text="已关闭", fg="gray")
    
    def toggle_auto_mode(self):
        """切换自动模式"""
        self.settings["auto_mode"] = self.auto_var.get()
        self.save_settings(self.settings)
        
        if self.settings["auto_mode"]:
            self.start_monitoring()
        else:
            self.stop_monitoring_thread()
            
        self.update_auto_status()

    def stop_monitoring_thread(self):
        """停止监控线程并等待其终止"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.stop_monitoring = True
            # 设置一个超时，避免无限等待
            wait_count = 0
            while self.monitoring_thread.is_alive() and wait_count < 10:
                time.sleep(0.1)
                wait_count += 1
            # 如果线程仍在运行，输出警告
            if self.monitoring_thread.is_alive():
                print("警告：监控线程未能在预期时间内终止")
            
    def start_monitoring(self):
        """开始监控剪贴板"""
        # 先确保之前的线程已停止
        self.stop_monitoring_thread()
            
        self.stop_monitoring = False
        self.last_clipboard_content = pyperclip.paste()
        
        self.monitoring_thread = threading.Thread(target=self.monitor_clipboard)
        self.monitoring_thread.daemon = True  # 设为守护线程，程序退出时自动结束
        self.monitoring_thread.start()
        
        self.status_label.config(text="自动模式已启动，正在监控剪贴板...")
    
    def monitor_clipboard(self):
        """监控剪贴板内容变化"""
        while not self.stop_monitoring:
            try:
                current_content = pyperclip.paste()
                
                # 如果剪贴板内容改变且不为空
                if current_content != self.last_clipboard_content and current_content.strip():
                    self.root.after(100, self.auto_replace_text, current_content)
                    self.last_clipboard_content = current_content
                    
            except Exception as e:
                # 处理可能的异常
                print(f"监控剪贴板时发生错误: {e}")
                
            # 间隔一段时间再检测
            time.sleep(self.settings["polling_interval"])
    
    def auto_replace_text(self, content):
        """自动替换文本（在主线程中执行）"""
        original_content = content
        
        # 应用所有替换规则
        replacements_count = 0
        for rule in self.settings["replacements"]:
            from_text = rule["from"]
            to_text = rule["to"]
            if from_text in content:
                count = content.count(from_text)
                content = content.replace(from_text, to_text)
                replacements_count += count
        
        # 如果有变化，将修改后的内容放回剪贴板
        if original_content != content and replacements_count > 0:
            # 临时停止监控以避免死循环
            temp_stop = self.stop_monitoring
            self.stop_monitoring = True
            
            pyperclip.copy(content)
            self.last_clipboard_content = content
            
            # 恢复监控状态
            self.stop_monitoring = temp_stop
            
            self.status_label.config(text=f"自动替换：共替换了 {replacements_count} 处内容")
    
    def update_rules_listbox(self):
        """更新替换规则列表显示"""
        self.rules_listbox.delete(0, tk.END)
        for rule in self.settings["replacements"]:
            self.rules_listbox.insert(tk.END, f"{rule['from']} → {rule['to']}")
    
    def replace_text(self):
        """手动执行文本替换"""
        # 获取剪贴板内容
        clipboard_content = pyperclip.paste()
        original_content = clipboard_content
        
        # 应用所有替换规则
        replacements_count = 0
        for rule in self.settings["replacements"]:
            from_text = rule["from"]
            to_text = rule["to"]
            if from_text in clipboard_content:
                count = clipboard_content.count(from_text)
                clipboard_content = clipboard_content.replace(from_text, to_text)
                replacements_count += count
        
        # 将修改后的内容放回剪贴板
        if original_content != clipboard_content:
            pyperclip.copy(clipboard_content)
            self.status_label.config(text=f"替换完成：共替换了 {replacements_count} 处内容")
        else:
            self.status_label.config(text="剪贴板中没有找到需要替换的内容")
    
    def add_replacement(self):
        """添加新的替换规则"""
        from_text = simpledialog.askstring("添加替换规则", "请输入要查找的文本:")
        if from_text:
            to_text = simpledialog.askstring("添加替换规则", f"将 '{from_text}' 替换为:")
            if to_text is not None:  # 用户可能输入空字符串作为替换值
                self.settings["replacements"].append({"from": from_text, "to": to_text})
                self.save_settings(self.settings)
                self.update_rules_listbox()
                self.status_label.config(text=f"已添加替换规则: '{from_text}' → '{to_text}'")
    
    def edit_replacements(self):
        """编辑替换规则窗口"""
        if not self.settings["replacements"]:
            messagebox.showinfo("提示", "没有替换规则可编辑")
            return
            
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑替换规则")
        edit_window.geometry("400x300")
        edit_window.grab_set()  # 模态窗口
        
        # 创建列表框
        list_frame = tk.Frame(edit_window)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        rules_listbox = tk.Listbox(list_frame, width=40, height=10)
        rules_listbox.pack(padx=20, fill=tk.BOTH, expand=True)
        
        # 填充列表
        for rule in self.settings["replacements"]:
            rules_listbox.insert(tk.END, f"{rule['from']} → {rule['to']}")
        
        # 按钮框
        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=5)
        
        # 编辑按钮
        def edit_selected():
            selected_idx = rules_listbox.curselection()
            if not selected_idx:
                return
                
            idx = selected_idx[0]
            rule = self.settings["replacements"][idx]
            
            new_from = simpledialog.askstring("编辑", "查找文本:", 
                                             initialvalue=rule["from"])
            if new_from is not None:
                new_to = simpledialog.askstring("编辑", "替换为:", 
                                               initialvalue=rule["to"])
                if new_to is not None:
                    self.settings["replacements"][idx] = {"from": new_from, "to": new_to}
                    self.save_settings(self.settings)
                    
                    # 更新显示
                    rules_listbox.delete(idx)
                    rules_listbox.insert(idx, f"{new_from} → {new_to}")
                    self.update_rules_listbox()
        
        # 删除按钮
        def delete_selected():
            selected_idx = rules_listbox.curselection()
            if not selected_idx:
                return
                
            idx = selected_idx[0]
            if messagebox.askyesno("确认", f"确定要删除规则 '{self.settings['replacements'][idx]['from']} → {self.settings['replacements'][idx]['to']}' 吗?"):
                del self.settings["replacements"][idx]
                self.save_settings(self.settings)
                rules_listbox.delete(idx)
                self.update_rules_listbox()
        
        edit_btn = tk.Button(button_frame, text="编辑", command=edit_selected)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(button_frame, text="删除", command=delete_selected)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(button_frame, text="关闭", command=edit_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def auto_mode_settings(self):
        """自动模式设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("自动模式设置")
        settings_window.geometry("300x150")
        settings_window.grab_set()  # 模态窗口
        
        # 创建设置框
        settings_frame = tk.Frame(settings_window)
        settings_frame.pack(pady=20, padx=20, fill=tk.BOTH)
        
        # 检测间隔设置
        interval_frame = tk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(interval_frame, text="检测间隔 (秒):").pack(side=tk.LEFT)
        
        interval_var = tk.DoubleVar(value=self.settings["polling_interval"])
        interval_spin = tk.Spinbox(
            interval_frame, 
            from_=0.1, 
            to=5.0, 
            increment=0.1, 
            textvariable=interval_var,
            width=5
        )
        interval_spin.pack(side=tk.LEFT, padx=5)
        
        # 按钮框
        button_frame = tk.Frame(settings_window)
        button_frame.pack(pady=20)
        
        def save_settings():
            self.settings["polling_interval"] = interval_var.get()
            self.save_settings(self.settings)
            settings_window.destroy()
            
            # 如果自动模式正在运行，重启监控线程以应用新设置
            if self.settings["auto_mode"]:
                self.stop_monitoring = True
                time.sleep(self.settings["polling_interval"] * 2)  # 确保旧线程已停止
                self.start_monitoring()
        
        save_btn = tk.Button(button_frame, text="保存", command=save_settings)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="取消", command=settings_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def reset_settings(self):
        """恢复默认设置"""
        if messagebox.askyesno("确认", "确定要恢复默认设置吗?"):
            # 如果正在监控，先停止
            if self.settings["auto_mode"]:
                self.stop_monitoring = True
            
            self.settings = self.default_settings.copy()
            self.save_settings(self.settings)
            
            # 更新UI
            self.auto_var.set(self.settings["auto_mode"])
            self.update_auto_status()
            self.update_rules_listbox()
            
            # 如果默认开启自动模式，则重新启动监控
            if self.settings["auto_mode"]:
                self.start_monitoring()
                
            self.status_label.config(text="已恢复默认设置")
    
    def on_closing(self):
        """窗口关闭事件处理"""
        # 停止监控线程
        self.stop_monitoring = True
        # 等待线程终止，但设置超时避免阻塞
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=1.0)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardReplacer(root)
    root.mainloop()
