import pyperclip
import time
import tkinter as tk
from tkinter import messagebox

def replace_text():
    # 获取剪贴板内容
    clipboard_content = pyperclip.paste()
    
    # 替换文本
    new_content = clipboard_content.replace("hduser", "hduse")
    
    # 将修改后的内容放回剪贴板
    pyperclip.copy(new_content)
    
    # 更新状态标签
    if clipboard_content != new_content:
        status_label.config(text=f"替换完成：找到并替换了 {clipboard_content.count('hduser')} 处 'hduser'")
    else:
        status_label.config(text="剪贴板中没有找到 'hduser'")

# 创建简单的GUI界面
root = tk.Tk()
root.title("剪贴板文本替换工具")
root.geometry("300x150")
root.resizable(False, False)

# 添加说明标签
instruction = tk.Label(root, text="点击按钮将剪贴板中的'hduser'替换为'hduse'", wraplength=250)
instruction.pack(pady=10)

# 创建替换按钮
replace_button = tk.Button(root, text="执行替换", command=replace_text)
replace_button.pack(pady=10)

# 创建状态标签
status_label = tk.Label(root, text="准备就绪")
status_label.pack(pady=10)

# 启动GUI主循环
root.mainloop()
