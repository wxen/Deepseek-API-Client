#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DeepSeek API 客户端 (GUI 版本)
使用 Python 和 Tkinter 实现的可视化界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import requests
import os
import time

class DeepSeekClient:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepSeek API 客户端")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 配置数据
        self.config = {
            "api_key": "YOUR_API_KEY_HERE",
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        # 会话数据
        self.sessions = {}
        self.current_session = "默认会话"
        
        # 加载配置和会话
        self.load_config()
        self.load_sessions()
        
        # 创建主框架
        self.create_main_frame()
        
    def create_main_frame(self):
        """创建主框架"""
        # 创建分割视图
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧会话管理面板
        self.session_frame = ttk.Frame(self.paned_window, width=250)
        self.paned_window.add(self.session_frame, weight=1)
        
        # 右侧聊天和配置面板
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, weight=3)
        
        # 创建标签页
        self.tab_control = ttk.Notebook(self.right_frame)
        self.chat_tab = ttk.Frame(self.tab_control)
        self.config_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.chat_tab, text="聊天")
        self.tab_control.add(self.config_tab, text="配置")
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # 创建会话管理面板
        self.create_session_panel()
        
        # 创建聊天面板
        self.create_chat_panel()
        
        # 创建配置面板
        self.create_config_panel()
        
        # 创建状态栏
        self.status_frame = ttk.Frame(self.root, height=20)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = ttk.Label(self.status_frame, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
    
    def create_session_panel(self):
        """创建会话管理面板"""
        # 会话标题 - 使用 Windows 通用字体
        try:
            ttk.Label(self.session_frame, text="会话管理", font=("Microsoft YaHei", 12, "bold")).pack(pady=10)
        except:
            try:
                ttk.Label(self.session_frame, text="会话管理", font=("SimHei", 12, "bold")).pack(pady=10)
            except:
                ttk.Label(self.session_frame, text="会话管理", font=("Arial", 12, "bold")).pack(pady=10)
        
        # 会话列表
        self.session_listbox = tk.Listbox(self.session_frame, height=15)
        self.session_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.update_session_list()
        
        # 会话操作按钮
        button_frame = ttk.Frame(self.session_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 会话名称输入框
        self.session_name_var = tk.StringVar()
        ttk.Entry(button_frame, textvariable=self.session_name_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # 新建会话按钮
        ttk.Button(button_frame, text="新建", command=self.create_session).pack(side=tk.LEFT, padx=5)
        
        # 删除会话按钮
        ttk.Button(button_frame, text="删除", command=self.delete_session).pack(side=tk.LEFT, padx=5)
        
        # 切换会话事件
        self.session_listbox.bind("<<ListboxSelect>>", self.switch_session)
    
    def create_chat_panel(self):
        """创建聊天面板"""
        # 聊天历史
        self.chat_history = scrolledtext.ScrolledText(self.chat_tab, wrap=tk.WORD, height=20)
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_history.config(state=tk.DISABLED)
        
        # 消息操作提示
        message_hint_frame = ttk.Frame(self.chat_tab)
        message_hint_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(message_hint_frame, text="操作提示: 使用方向键选择消息，按空格键编辑，按Ctrl+Enter发送消息").pack(side=tk.LEFT, padx=5)
        
        # 消息输入框
        input_frame = ttk.Frame(self.chat_tab)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 使用ScrolledText支持多行输入
        self.message_entry = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=4)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 发送按钮
        ttk.Button(input_frame, text="发送", command=self.send_message).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 绑定组合键发送消息（Ctrl+Enter）
        self.message_entry.bind("<Control-Return>", lambda event: self.send_message())
        # 确保按Enter键换行，而不是发送消息
        self.message_entry.bind("<Return>", lambda event: "break")
    
    def create_config_panel(self):
        """创建配置面板"""
        # 配置表单
        config_frame = ttk.Frame(self.config_tab, padding=20)
        config_frame.pack(fill=tk.BOTH, expand=True)
        
        # API Key
        ttk.Label(config_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar(value="YOUR_API_KEY_HERE")
        ttk.Entry(config_frame, textvariable=self.api_key_var, width=50).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 模型
        ttk.Label(config_frame, text="模型:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value=self.config["model"])
        ttk.Entry(config_frame, textvariable=self.model_var, width=50).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 温度
        ttk.Label(config_frame, text="温度:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.temperature_var = tk.DoubleVar(value=self.config["temperature"])
        ttk.Scale(config_frame, from_=0.0, to=2.0, orient=tk.HORIZONTAL, variable=self.temperature_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        ttk.Label(config_frame, textvariable=self.temperature_var).grid(row=2, column=2, sticky=tk.W, pady=5)
        
        # 最大Tokens
        ttk.Label(config_frame, text="最大Tokens:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.max_tokens_var = tk.IntVar(value=self.config["max_tokens"])
        ttk.Entry(config_frame, textvariable=self.max_tokens_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Top P
        ttk.Label(config_frame, text="Top P:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.top_p_var = tk.DoubleVar(value=self.config["top_p"])
        ttk.Scale(config_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.top_p_var).grid(row=4, column=1, sticky=tk.W, pady=5)
        ttk.Label(config_frame, textvariable=self.top_p_var).grid(row=4, column=2, sticky=tk.W, pady=5)
        
        # 频率惩罚
        ttk.Label(config_frame, text="频率惩罚:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.frequency_penalty_var = tk.IntVar(value=self.config["frequency_penalty"])
        ttk.Entry(config_frame, textvariable=self.frequency_penalty_var, width=10).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # 存在惩罚
        ttk.Label(config_frame, text="存在惩罚:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.presence_penalty_var = tk.IntVar(value=self.config["presence_penalty"])
        ttk.Entry(config_frame, textvariable=self.presence_penalty_var, width=10).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # 保存配置按钮
        ttk.Button(config_frame, text="保存配置", command=self.save_config).grid(row=7, column=0, columnspan=3, pady=20)
    
    def update_session_list(self):
        """更新会话列表"""
        self.session_listbox.delete(0, tk.END)
        for session in self.sessions:
            if session == self.current_session:
                self.session_listbox.insert(tk.END, f"{session} [当前]")
            else:
                self.session_listbox.insert(tk.END, session)
    
    def create_session(self):
        """创建新会话"""
        session_name = self.session_name_var.get()
        if not session_name:
            session_name = f"会话_{int(time.time())}"
        
        if session_name not in self.sessions:
            self.sessions[session_name] = []
            self.current_session = session_name
            self.update_session_list()
            self.update_chat_history()
            self.session_name_var.set("")
            self.save_sessions()
    
    def delete_session(self):
        """删除会话"""
        selected = self.session_listbox.curselection()
        if selected:
            # 获取选中的会话项文本
            session_item = self.session_listbox.get(selected[0])
            # 提取实际会话名称（移除" [当前]"标记）
            session_name = session_item.replace(" [当前]", "")
            
            if session_name != "默认会话":
                # 确保会话存在于字典中
                if session_name in self.sessions:
                    # 删除会话
                    del self.sessions[session_name]
                    # 如果删除的是当前会话，切换到默认会话
                    if session_name == self.current_session:
                        self.current_session = "默认会话"
                    # 更新会话列表和聊天历史
                    self.update_session_list()
                    self.update_chat_history()
                    # 保存会话
                    self.save_sessions()
                    # 显示成功消息
                    self.status_label.config(text=f"会话 '{session_name}' 已删除")
                else:
                    # 显示错误消息
                    messagebox.showerror("错误", f"会话 '{session_name}' 不存在")
            else:
                messagebox.showinfo("提示", "默认会话不能删除")
        else:
            messagebox.showinfo("提示", "请先选择要删除的会话")
    
    def switch_session(self, event):
        """切换会话"""
        selected = self.session_listbox.curselection()
        if selected:
            session_name = self.session_listbox.get(selected[0])
            if " [当前]" in session_name:
                session_name = session_name.replace(" [当前]", "")
            
            if session_name in self.sessions:
                self.current_session = session_name
                self.update_session_list()
                self.update_chat_history()
    
    def update_chat_history(self):
        """更新聊天历史"""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        
        if self.current_session in self.sessions:
            for i, message in enumerate(self.sessions[self.current_session]):
                role = message["role"]
                content = message["content"]
                timestamp = message.get("timestamp", "")
                
                # 添加消息标签，格式为"msg_{index}"
                msg_tag = f"msg_{i}"
                
                if role == "user":
                    self.chat_history.insert(tk.END, f"用户: {content}\n", ("user", msg_tag))
                elif role == "assistant":
                    self.chat_history.insert(tk.END, f"助手: {content}\n", ("assistant", msg_tag))
                elif role == "system":
                    self.chat_history.insert(tk.END, f"系统: {content}\n", ("system", msg_tag))
                
                if timestamp:
                    self.chat_history.insert(tk.END, f"时间: {timestamp}\n", "timestamp")
                
                self.chat_history.insert(tk.END, "-" * 80 + "\n")
        
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)
        
        # 绑定键盘事件
        self.chat_history.bind("<Up>", self.select_previous_message)
        self.chat_history.bind("<Down>", self.select_next_message)
        self.chat_history.bind("<space>", self.confirm_message_selection)
        
        # 初始化当前选中的消息索引
        self.selected_message_index = -1
    
    def send_message(self):
        """发送消息"""
        message = self.message_entry.get(1.0, tk.END).strip()
        if message:
            # 添加用户消息
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            user_message = {
                "role": "user",
                "content": message,
                "timestamp": timestamp
            }
            
            if self.current_session not in self.sessions:
                self.sessions[self.current_session] = []
            
            self.sessions[self.current_session].append(user_message)
            self.update_chat_history()
            self.message_entry.delete(1.0, tk.END)
            
            # 发送到API
            self.send_to_api()
            self.save_sessions()
    
    def send_to_api(self):
        """发送消息到API"""
        # 构建请求体
        messages = []
        
        # 添加系统消息
        messages.append({"role": "system", "content": "You are a helpful assistant."})
        
        # 添加对话历史
        if self.current_session in self.sessions:
            for msg in self.sessions[self.current_session]:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 构建请求数据
        data = {
            "model": self.config["model"],
            "messages": messages,
            "temperature": self.config["temperature"],
            "max_tokens": self.config["max_tokens"],
            "top_p": self.config["top_p"],
            "frequency_penalty": self.config["frequency_penalty"],
            "presence_penalty": self.config["presence_penalty"]
        }
        
        # 使用DeepSeek API
        api_key = self.api_key_var.get()
        api_endpoint = "https://api.deepseek.com/v1/chat/completions"
        
        # 发送请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        try:
            response = requests.post(
                api_endpoint,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result["choices"][0]["message"]["content"]
                
                # 添加助手消息
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                assistant_msg = {
                    "role": "assistant",
                    "content": assistant_message,
                    "timestamp": timestamp
                }
                
                self.sessions[self.current_session].append(assistant_msg)
                self.update_chat_history()
                self.save_sessions()
            else:
                # 添加错误消息
                error_message = f"API错误: {response.text} (状态码: {response.status_code})"
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                error_msg = {
                    "role": "system",
                    "content": error_message,
                    "timestamp": timestamp
                }
                
                self.sessions[self.current_session].append(error_msg)
                self.update_chat_history()
                self.save_sessions()
        except Exception as e:
            # 添加错误消息
            error_message = f"网络错误: {str(e)}"
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            error_msg = {
                "role": "system",
                "content": error_message,
                "timestamp": timestamp
            }
            
            self.sessions[self.current_session].append(error_msg)
            self.update_chat_history()
            self.save_sessions()
    
    def edit_message(self):
        """编辑消息"""
        # 简化实现，实际应用中可以添加更复杂的编辑功能
        messagebox.showinfo("提示", "编辑消息功能正在开发中")
    
    def delete_message(self):
        """删除消息"""
        # 简化实现，实际应用中可以添加更复杂的删除功能
        messagebox.showinfo("提示", "删除消息功能正在开发中")
    
    def select_previous_message(self, event):
        """选择上一条消息"""
        if self.current_session in self.sessions:
            num_messages = len(self.sessions[self.current_session])
            if num_messages > 0:
                # 取消当前选中消息的高亮
                if self.selected_message_index >= 0:
                    self.chat_history.tag_remove("sel", f"msg_{self.selected_message_index}.0", f"msg_{self.selected_message_index}.end")
                
                # 选择上一条消息
                if self.selected_message_index <= 0:
                    self.selected_message_index = num_messages - 1
                else:
                    self.selected_message_index -= 1
                
                # 高亮显示选中的消息，使用更明显的高亮样式
                self.chat_history.tag_configure("sel", background="#ffffcc", foreground="#000000")
                self.chat_history.tag_add("sel", f"msg_{self.selected_message_index}.0", f"msg_{self.selected_message_index}.end")
                self.chat_history.see(f"msg_{self.selected_message_index}.0")
                
                # 在状态栏显示当前选中的消息信息
                message = self.sessions[self.current_session][self.selected_message_index]
                role = message["role"]
                role_text = "用户" if role == "user" else "助手" if role == "assistant" else "系统"
                status_text = f"当前选中: 第{self.selected_message_index + 1}条消息 ({role_text})"
                # 更新状态栏
                if hasattr(self, "status_label"):
                    self.status_label.config(text=status_text)
        return "break"
    
    def select_next_message(self, event):
        """选择下一条消息"""
        if self.current_session in self.sessions:
            num_messages = len(self.sessions[self.current_session])
            if num_messages > 0:
                # 取消当前选中消息的高亮
                if self.selected_message_index >= 0:
                    self.chat_history.tag_remove("sel", f"msg_{self.selected_message_index}.0", f"msg_{self.selected_message_index}.end")
                
                # 选择下一条消息
                self.selected_message_index = (self.selected_message_index + 1) % num_messages
                
                # 高亮显示选中的消息，使用更明显的高亮样式
                self.chat_history.tag_configure("sel", background="#ffffcc", foreground="#000000")
                self.chat_history.tag_add("sel", f"msg_{self.selected_message_index}.0", f"msg_{self.selected_message_index}.end")
                self.chat_history.see(f"msg_{self.selected_message_index}.0")
                
                # 在状态栏显示当前选中的消息信息
                message = self.sessions[self.current_session][self.selected_message_index]
                role = message["role"]
                role_text = "用户" if role == "user" else "助手" if role == "assistant" else "系统"
                status_text = f"当前选中: 第{self.selected_message_index + 1}条消息 ({role_text})"
                # 更新状态栏
                if hasattr(self, "status_label"):
                    self.status_label.config(text=status_text)
        return "break"
    
    def confirm_message_selection(self, event):
        """确认选择并进入编辑模式"""
        if self.selected_message_index >= 0 and self.current_session in self.sessions:
            messages = self.sessions[self.current_session]
            if self.selected_message_index < len(messages):
                # 获取当前选中的消息
                message = messages[self.selected_message_index]
                
                # 创建编辑对话框
                edit_window = tk.Toplevel(self.root)
                edit_window.title("编辑消息")
                edit_window.geometry("500x300")
                
                # 添加标签
                ttk.Label(edit_window, text="消息内容:").pack(pady=10)
                
                # 添加文本框
                text_widget = scrolledtext.ScrolledText(edit_window, wrap=tk.WORD, height=10)
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                text_widget.insert(tk.END, message["content"])
                
                # 添加按钮
                button_frame = ttk.Frame(edit_window)
                button_frame.pack(fill=tk.X, pady=10)
                
                def save_changes():
                    # 获取编辑后的内容
                    new_content = text_widget.get(1.0, tk.END).strip()
                    if new_content:
                        # 更新消息内容
                        message["content"] = new_content
                        message["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        
                        # 保存更改
                        self.save_sessions()
                        self.update_chat_history()
                        
                        # 关闭对话框
                        edit_window.destroy()
                
                ttk.Button(button_frame, text="保存", command=save_changes).pack(side=tk.RIGHT, padx=10)
                ttk.Button(button_frame, text="取消", command=edit_window.destroy).pack(side=tk.RIGHT, padx=10)
        return "break"
    
    def save_config(self):
        """保存配置"""
        self.config["api_key"] = self.api_key_var.get()
        self.config["model"] = self.model_var.get()
        self.config["temperature"] = self.temperature_var.get()
        self.config["max_tokens"] = self.max_tokens_var.get()
        self.config["top_p"] = self.top_p_var.get()
        self.config["frequency_penalty"] = self.frequency_penalty_var.get()
        self.config["presence_penalty"] = self.presence_penalty_var.get()
        
        self.save_config_to_file()
        messagebox.showinfo("提示", "配置保存成功")
    
    def save_config_to_file(self):
        """保存配置到文件"""
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def load_config(self):
        """加载配置"""
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r", encoding="utf-8") as f:
                    self.config.update(json.load(f))
            except Exception as e:
                print(f"加载配置失败: {e}")
    
    def save_sessions(self):
        """保存会话到文件"""
        with open("sessions.json", "w", encoding="utf-8") as f:
            json.dump(self.sessions, f, ensure_ascii=False, indent=2)
    
    def load_sessions(self):
        """加载会话"""
        if os.path.exists("sessions.json"):
            try:
                with open("sessions.json", "r", encoding="utf-8") as f:
                    self.sessions = json.load(f)
            except Exception as e:
                print(f"加载会话失败: {e}")
        
        # 确保默认会话存在
        if "默认会话" not in self.sessions:
            self.sessions["默认会话"] = []

if __name__ == "__main__":
    root = tk.Tk()
    app = DeepSeekClient(root)
    root.mainloop()
