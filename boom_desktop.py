#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信消息轰炸脚本 - 桌面版 (GUI)
使用 pyautogui 自动化桌面版微信
"""
import time
import requests
import random
import pyautogui
import pyperclip
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
import threading


class WeChatDesktopBomber:
    def __init__(self):
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True
        
    def get_hitokoto(self) -> str:
        """从一言API获取随机句子"""
        try:
            url = "https://v1.hitokoto.cn/?c=a&c=b&c=c&c=d&c=e&c=f&c=g&c=h&c=i&c=j&c=k&c=l"
            response = requests.get(url, timeout=0.5)
            if response.status_code == 200:
                data = response.json()
                hitokoto = data.get('hitokoto', '')
                from_who = data.get('from_who', '')
                from_text = data.get('from', '')
                
                result = hitokoto
                if from_who:
                    result += f"\n—— {from_who}"
                elif from_text:
                    result += f"\n—— {from_text}"
                return result
            else:
                return self.get_backup_message()
        except Exception as e:
            return self.get_backup_message()
    
    def get_backup_message(self) -> str:
        """备用消息列表"""
        backup_messages = [
            "岁月不居，时节如流。",
            "愿你出走半生，归来仍是少年。",
            "生活不止眼前的苟且，还有诗和远方。",
            "星光不负赶路人。",
            "心之所向，素履以往。"
        ]
        return random.choice(backup_messages)
    
    def generate_messages(self, mode: str, count: int, fixed_text: str = "", progress_callback=None) -> List[str]:
        """生成消息列表"""
        messages = []
        
        if mode == 'fixed':
            messages = [fixed_text] * count
        elif mode == 'hitokoto':
            for i in range(count):
                msg = self.get_hitokoto()
                messages.append(msg)
                if i < count - 1:
                    time.sleep(1.0)
                if progress_callback:
                    progress_callback(i + 1, count)
        
        return messages
    
    def find_and_open_contact(self, name: str) -> bool:
        """查找并打开联系人或群聊"""
        print(f"\n请在10秒内切换到微信窗口...")
        time.sleep(10)
        
        try:
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(1)
            
            pyperclip.copy(name)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)
            
            pyautogui.press('enter')
            time.sleep(2)
            
            pyautogui.press('enter')
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"打开聊天窗口失败: {e}")
            return False
    
    def send_messages(self, messages: List[str], interval: float = 0.1, progress_callback=None):
        """发送消息"""
        success_count = 0
        fail_count = 0
        
        for i, msg in enumerate(messages):
            try:
                pyperclip.copy(msg)
                time.sleep(0.05)
                
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.05)
                
                pyautogui.press('enter')
                success_count += 1
                
                time.sleep(interval)
                
                if progress_callback:
                    progress_callback(i + 1, len(messages))
                    
            except Exception as e:
                fail_count += 1
        
        return success_count, fail_count


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("微信消息轰炸工具")
        self.root.geometry("400x420")
        self.root.resizable(False, False)
        
        self.bomber = WeChatDesktopBomber()
        self.is_running = False
        
        self._build_ui()
        
    def _build_ui(self):
        # 标题
        title_label = tk.Label(self.root, text="微信消息轰炸工具", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=15)
        
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=30, fill="x")
        
        # 目标名称
        ttk.Label(main_frame, text="目标名称:").grid(row=0, column=0, sticky="w", pady=8)
        self.target_entry = ttk.Entry(main_frame, width=30)
        self.target_entry.grid(row=0, column=1, pady=8)
        
        # 消息模式
        ttk.Label(main_frame, text="消息模式:").grid(row=1, column=0, sticky="w", pady=8)
        self.msg_mode = tk.StringVar(value="hitokoto")
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=1, column=1, sticky="w", pady=8)
        ttk.Radiobutton(mode_frame, text="一言API", variable=self.msg_mode, value="hitokoto").pack(side="left")
        ttk.Radiobutton(mode_frame, text="固定内容", variable=self.msg_mode, value="fixed").pack(side="left", padx=10)
        self.msg_mode.trace("w", self._on_mode_change)
        
        # 固定消息内容
        self.fixed_frame = ttk.Frame(main_frame)
        self.fixed_frame.grid(row=2, column=0, columnspan=2, sticky="we", pady=8)
        ttk.Label(self.fixed_frame, text="固定消息:").pack(anchor="w")
        self.fixed_text = tk.Text(self.fixed_frame, width=38, height=3)
        self.fixed_text.pack(pady=5)
        self.fixed_frame.grid_remove()  # 初始隐藏
        
        # 发送次数
        ttk.Label(main_frame, text="发送次数:").grid(row=3, column=0, sticky="w", pady=8)
        self.count_entry = ttk.Entry(main_frame, width=15)
        self.count_entry.insert(0, "10")
        self.count_entry.grid(row=3, column=1, sticky="w", pady=8)
        
        # 发送间隔
        ttk.Label(main_frame, text="发送间隔(秒):").grid(row=4, column=0, sticky="w", pady=8)
        self.interval_entry = ttk.Entry(main_frame, width=15)
        self.interval_entry.insert(0, "0.1")
        self.interval_entry.grid(row=4, column=1, sticky="w", pady=8)
        
        # 提示信息
        tip_label = tk.Label(main_frame, text="提示: 移动鼠标到左上角可紧急停止", 
                             font=("微软雅黑", 9), foreground="gray")
        tip_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, length=340, mode="determinate")
        self.progress.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="就绪", font=("微软雅黑", 10))
        self.status_label.pack(pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.start_btn = ttk.Button(btn_frame, text="开始发送", command=self._start)
        self.start_btn.pack(side="left", padx=10)
        ttk.Button(btn_frame, text="退出", command=self.root.quit).pack(side="left", padx=10)
        
    def _on_mode_change(self, *args):
        if self.msg_mode.get() == "fixed":
            self.fixed_frame.grid()
        else:
            self.fixed_frame.grid_remove()
    
    def _update_status(self, text):
        self.status_label.config(text=text)
        self.root.update()
    
    def _update_progress(self, current, total):
        self.progress["value"] = (current / total) * 100
        self.status_label.config(text=f"已发送: {current}/{total}")
        self.root.update()
    
    def _start(self):
        if self.is_running:
            return
            
        # 获取参数
        name = self.target_entry.get().strip()
        mode = self.msg_mode.get()
        count_str = self.count_entry.get().strip()
        interval_str = self.interval_entry.get().strip()
        
        # 验证参数
        if not name:
            messagebox.showwarning("提示", "请输入目标名称！")
            return
        
        try:
            count = int(count_str)
            if count <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("提示", "发送次数必须是正整数！")
            return
        
        try:
            interval = float(interval_str)
            if interval < 0:
                interval = 0.1
        except ValueError:
            interval = 0.1
        
        fixed_text = ""
        if mode == "fixed":
            fixed_text = self.fixed_text.get("1.0", "end").strip()
            if not fixed_text:
                messagebox.showwarning("提示", "请输入固定消息内容！")
                return
        
        # 确认
        msg_type = "固定内容" if mode == "fixed" else "一言API"
        confirm = messagebox.askyesno("确认", 
            f"目标: {name}\n消息模式: {msg_type}\n发送次数: {count}\n发送间隔: {interval}秒\n\n确认开始发送？")
        
        if not confirm:
            return
        
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.progress["value"] = 0
        
        # 在新线程中执行
        thread = threading.Thread(target=self._run_bombing, args=(name, mode, count, interval, fixed_text))
        thread.daemon = True
        thread.start()
    
    def _run_bombing(self, name, mode, count, interval, fixed_text):
        try:
            self._update_status("正在生成消息...")
            messages = self.bomber.generate_messages(mode, count, fixed_text)
            
            self._update_status("请切换到微信窗口...")
            time.sleep(1)
            
            if not self.bomber.find_and_open_contact(name):
                self._update_status("打开聊天窗口失败")
                messagebox.showerror("错误", "打开聊天窗口失败，请重试！")
                self.is_running = False
                self.start_btn.config(state="normal")
                return
            
            self._update_status("正在发送...")
            success, fail = self.bomber.send_messages(messages, interval, self._update_progress)
            
            self._update_status(f"完成! 成功:{success} 失败:{fail}")
            messagebox.showinfo("完成", f"发送完成！\n成功: {success}\n失败: {fail}")
            
        except pyautogui.FailSafeException:
            self._update_status("用户中断")
            messagebox.showinfo("提示", "程序已中断")
        except Exception as e:
            self._update_status(f"错误: {e}")
            messagebox.showerror("错误", str(e))
        finally:
            self.is_running = False
            self.start_btn.config(state="normal")
    
    def run(self):
        self.root.mainloop()


def main():
    try:
        gui = GUI()
        gui.run()
    except Exception as e:
        print(f"程序出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
