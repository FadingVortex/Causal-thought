import pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ClipboardReplacer:
    def __init__(self, root):
        self.root = root
        self.root.title("剪贴板文本替换工具")
        self.root.geometry("360x320")
        self.root.resizable(False, False)
        
        # 默认替换设置
        self.default_settings = {"replacements": [{"from": "hduser", "to": "hduse"}]}
        self.settings_file = "replacer_settings.json"
        self.settings = self.load_settings()
        
        self.create_widgets()
        
    def load_settings(self):
        """加载设置，如果文件不存在则创建默认设置"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
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
        settings_menu.add_separator()
        settings_menu.add_command(label="恢复默认设置", command=self.reset_settings)
        
        # 添加说明标签
        self.instruction = tk.Label(self.root, text="点击按钮将自动替换剪贴板中的文本", wraplength=300)
        self.instruction.pack(pady=10)
        
        # 创建替换按钮
        self.replace_button = tk.Button(self.root, text="执行替换", command=self.replace_text, height=2, width=15)
        self.replace_button.pack(pady=10)
        
        # 创建状态标签
        self.status_label = tk.Label(self.root, text="准备就绪")
        self.status_label.pack(pady=10)
        
        # 创建替换规则列表框
        self.rules_frame = tk.Frame(self.root)
        self.rules_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.rules_label = tk.Label(self.rules_frame, text="当前替换规则:")
        self.rules_label.pack(anchor=tk.W, padx=20)
        
        self.rules_listbox = tk.Listbox(self.rules_frame, width=40, height=8)
        self.rules_listbox.pack(padx=20, fill=tk.BOTH, expand=True)
        
        # 更新替换规则列表显示
        self.update_rules_listbox()
    
    def update_rules_listbox(self):
        """更新替换规则列表显示"""
        self.rules_listbox.delete(0, tk.END)
        for rule in self.settings["replacements"]:
            self.rules_listbox.insert(tk.END, f"{rule['from']} → {rule['to']}")
    
    def replace_text(self):
        """执行文本替换"""
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
    
    def reset_settings(self):
        """恢复默认设置"""
        if messagebox.askyesno("确认", "确定要恢复默认设置吗?"):
            self.settings = self.default_settings.copy()
            self.save_settings(self.settings)
            self.update_rules_listbox()
            self.status_label.config(text="已恢复默认设置")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardReplacer(root)
    root.mainloop()
