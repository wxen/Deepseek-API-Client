#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DeepSeek API 客户端 (终端版本)
使用 Python 实现的命令行界面
"""

import json
import requests
import os
import time
import sys

class DeepSeekCLIClient:
    def __init__(self):
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
    
    def load_config(self):
        """加载配置"""
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r", encoding="utf-8") as f:
                    self.config.update(json.load(f))
            except Exception as e:
                print(f"加载配置失败: {e}")
    
    def save_config(self):
        """保存配置"""
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print("配置保存成功")
        except Exception as e:
            print(f"保存配置失败: {e}")
    
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
    
    def save_sessions(self):
        """保存会话"""
        try:
            with open("sessions.json", "w", encoding="utf-8") as f:
                json.dump(self.sessions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存会话失败: {e}")
    
    def print_main_menu(self):
        """打印主菜单"""
        print("\n===== DeepSeek API 客户端 =====")
        print("1. 会话管理")
        print("2. 聊天")
        print("3. 配置管理")
        print("4. 退出")
    
    def handle_main_menu(self):
        """处理主菜单"""
        while True:
            self.print_main_menu()
            choice = input("请输入选择: ")
            
            if choice == "1":
                self.handle_session_menu()
            elif choice == "2":
                self.handle_chat_menu()
            elif choice == "3":
                self.handle_config_menu()
            elif choice == "4":
                print("再见！")
                break
            else:
                print("无效选择，请重新输入")
    
    def print_session_menu(self):
        """打印会话菜单"""
        print("\n===== 会话管理 =====")
        print("1. 列出所有会话")
        print("2. 创建新会话")
        print("3. 删除会话")
        print("4. 切换会话")
        print("5. 返回主菜单")
    
    def handle_session_menu(self):
        """处理会话菜单"""
        while True:
            self.print_session_menu()
            choice = input("请输入选择: ")
            
            if choice == "1":
                self.list_sessions()
            elif choice == "2":
                self.create_session()
            elif choice == "3":
                self.delete_session()
            elif choice == "4":
                self.switch_session()
            elif choice == "5":
                break
            else:
                print("无效选择，请重新输入")
    
    def list_sessions(self):
        """列出所有会话"""
        print("\n===== 会话列表 =====")
        for session in self.sessions:
            if session == self.current_session:
                print(f"{session} [当前]")
            else:
                print(session)
        print()
    
    def create_session(self):
        """创建新会话"""
        session_name = input("请输入会话名称: ")
        if not session_name:
            session_name = f"会话_{int(time.time())}"
        
        if session_name not in self.sessions:
            self.sessions[session_name] = []
            self.current_session = session_name
            print(f"会话 '{session_name}' 创建成功")
            self.save_sessions()
        else:
            print(f"会话 '{session_name}' 已存在")
    
    def delete_session(self):
        """删除会话"""
        self.list_sessions()
        session_name = input("请输入要删除的会话名称: ")
        
        if session_name == "默认会话":
            print("默认会话不能删除")
        elif session_name in self.sessions:
            del self.sessions[session_name]
            if session_name == self.current_session:
                self.current_session = "默认会话"
            print(f"会话 '{session_name}' 删除成功")
            self.save_sessions()
        else:
            print(f"会话 '{session_name}' 不存在")
    
    def switch_session(self):
        """切换会话"""
        self.list_sessions()
        session_name = input("请输入要切换的会话名称: ")
        
        if session_name in self.sessions:
            self.current_session = session_name
            print(f"已切换到会话 '{session_name}'")
        else:
            print(f"会话 '{session_name}' 不存在")
    
    def print_chat_menu(self):
        """打印聊天菜单"""
        print("\n===== 聊天 =====")
        print(f"当前会话: {self.current_session}")
        print("1. 查看聊天历史")
        print("2. 发送消息")
        print("3. 编辑消息")
        print("4. 删除消息")
        print("5. 返回主菜单")
    
    def handle_chat_menu(self):
        """处理聊天菜单"""
        while True:
            self.print_chat_menu()
            choice = input("请输入选择: ")
            
            if choice == "1":
                self.list_messages()
            elif choice == "2":
                self.send_message()
            elif choice == "3":
                self.edit_message()
            elif choice == "4":
                self.delete_message()
            elif choice == "5":
                break
            else:
                print("无效选择，请重新输入")
    
    def list_messages(self):
        """查看聊天历史"""
        print(f"\n===== 聊天历史 - {self.current_session} =====")
        
        if not self.sessions[self.current_session]:
            print("聊天历史为空")
            return
        
        for i, message in enumerate(self.sessions[self.current_session]):
            role = message["role"]
            content = message["content"]
            timestamp = message.get("timestamp", "")
            
            role_text = "用户" if role == "user" else "助手" if role == "assistant" else "系统"
            print(f"[{i+1}] {role_text}: {content}")
            if timestamp:
                print(f"时间: {timestamp}")
            print("-" * 60)
    
    def send_message(self):
        """发送消息"""
        print(f"\n===== 发送消息 - {self.current_session} =====")
        print("请输入消息内容 (输入空行结束，输入 'exit' 退出):")
        
        # 支持多行输入
        message_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "exit":
                    return
                if not line:  # 空行结束输入
                    break
                message_lines.append(line)
            except EOFError:
                break
        
        message = "\n".join(message_lines)
        if not message:
            return
        
        # 添加用户消息
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        user_message = {
            "role": "user",
            "content": message,
            "timestamp": timestamp
        }
        
        self.sessions[self.current_session].append(user_message)
        print("\n发送中...")
        
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
        
        # 发送请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}"
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
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
                print("\n助手:", assistant_message)
                print("-" * 60)
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
                print("\n错误:", error_message)
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
            print("\n错误:", error_message)
    
    def edit_message(self):
        """编辑消息"""
        self.list_messages()
        
        try:
            msg_index = int(input("请输入要编辑的消息序号: ")) - 1
            if msg_index < 0 or msg_index >= len(self.sessions[self.current_session]):
                print("无效的消息序号")
                return
            
            message = self.sessions[self.current_session][msg_index]
            print(f"\n当前消息内容:")
            print(message["content"])
            print("\n请输入新的消息内容 (输入 'exit' 退出):")
            
            # 支持多行输入
            new_lines = []
            while True:
                line = input()
                if line.strip() == "exit":
                    break
                new_lines.append(line)
            
            new_content = "\n".join(new_lines)
            if new_content:
                message["content"] = new_content
                message["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
                print("消息编辑成功")
                self.save_sessions()
        except ValueError:
            print("无效的输入")
    
    def delete_message(self):
        """删除消息"""
        self.list_messages()
        
        try:
            msg_index = int(input("请输入要删除的消息序号: ")) - 1
            if msg_index < 0 or msg_index >= len(self.sessions[self.current_session]):
                print("无效的消息序号")
                return
            
            self.sessions[self.current_session].pop(msg_index)
            print("消息删除成功")
            self.save_sessions()
        except ValueError:
            print("无效的输入")
    
    def print_config_menu(self):
        """打印配置菜单"""
        print("\n===== 配置管理 =====")
        print("1. 查看当前配置")
        print("2. 编辑配置")
        print("3. 返回主菜单")
    
    def handle_config_menu(self):
        """处理配置菜单"""
        while True:
            self.print_config_menu()
            choice = input("请输入选择: ")
            
            if choice == "1":
                self.show_config()
            elif choice == "2":
                self.edit_config()
            elif choice == "3":
                break
            else:
                print("无效选择，请重新输入")
    
    def show_config(self):
        """查看当前配置"""
        print("\n===== 当前配置 =====")
        for key, value in self.config.items():
            print(f"{key}: {value}")
        print()
    
    def edit_config(self):
        """编辑配置"""
        print("\n===== 编辑配置 =====")
        print("请输入要修改的配置项 (输入 'exit' 退出):")
        print("可用配置项: api_key, model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty")
        
        while True:
            key = input("配置项: ")
            if key == "exit":
                break
            
            if key in self.config:
                current_value = self.config[key]
                print(f"当前值: {current_value}")
                
                new_value = input("新值: ")
                if new_value:
                    # 根据配置项类型转换值
                    if key in ["temperature", "top_p"]:
                        try:
                            self.config[key] = float(new_value)
                        except ValueError:
                            print("无效的数值，请输入数字")
                            continue
                    elif key in ["max_tokens", "frequency_penalty", "presence_penalty"]:
                        try:
                            self.config[key] = int(new_value)
                        except ValueError:
                            print("无效的数值，请输入整数")
                            continue
                    else:
                        self.config[key] = new_value
                    
                    print(f"{key} 已更新为: {self.config[key]}")
            else:
                print("无效的配置项")
        
        self.save_config()

if __name__ == "__main__":
    client = DeepSeekCLIClient()
    client.handle_main_menu()
