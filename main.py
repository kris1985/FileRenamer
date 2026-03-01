#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量重命名工具
主要功能：
1. 批量重命名文件（品牌_文件夹名称_日期_编号格式）
2. 清理文件名中的"副图_1"字符串
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
from pathlib import Path
import threading


class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件批量重命名工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="文件批量重命名工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 创建Notebook（标签页）
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # 功能1：批量重命名文件
        self.setup_batch_rename_tab(notebook)
        
        # 功能2：清理文件名
        self.setup_clean_filename_tab(notebook)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def setup_batch_rename_tab(self, notebook):
        """设置批量重命名功能标签页"""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="批量重命名")
        
        # 说明
        desc_label = ttk.Label(frame, text="功能：批量重命名文件为 品牌_文件夹名称_yyyy年MM月dd日_五位编号_副图1 格式（全局按修改时间排序）", 
                              font=("Arial", 10), foreground="blue")
        desc_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # 文件夹选择
        ttk.Label(frame, text="目标文件夹:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.rename_folder_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rename_folder_var, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(frame, text="浏览", command=self.browse_rename_folder).grid(
            row=1, column=2, pady=5)
        
        # 日期选择
        ttk.Label(frame, text="日期:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 5), pady=5)
        
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%Y年%m月%d日"))
        ttk.Entry(date_frame, textvariable=self.date_var, width=15).grid(row=0, column=0)
        ttk.Button(date_frame, text="今天", command=self.set_today_date).grid(
            row=0, column=1, padx=(5, 0))
        
        # 编号起始值
        ttk.Label(frame, text="编号起始值:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.start_number_var = tk.StringVar()
        self.start_number_var.set("10000")
        ttk.Entry(frame, textvariable=self.start_number_var, width=15).grid(
            row=3, column=1, sticky=tk.W, padx=(10, 5), pady=5)
        
        # 执行按钮
        ttk.Button(frame, text="开始批量重命名", command=self.batch_rename,
                  style="Accent.TButton").grid(row=4, column=1, pady=20)
        
        # 配置网格权重
        frame.columnconfigure(1, weight=1)
        
    def setup_clean_filename_tab(self, notebook):
        """设置清理文件名功能标签页"""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="清理文件名")
        
        # 说明
        desc_label = ttk.Label(frame, text="功能：清理文件名中的指定字符串（如'_副图1'）", 
                              font=("Arial", 10), foreground="blue")
        desc_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # 文件夹选择
        ttk.Label(frame, text="目标文件夹:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.clean_folder_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.clean_folder_var, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(frame, text="浏览", command=self.browse_clean_folder).grid(
            row=1, column=2, pady=5)
        
        # 自定义替换字符串
        ttk.Label(frame, text="要替换的字符串:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.replace_string_var = tk.StringVar()
        self.replace_string_var.set("_副图1")
        ttk.Entry(frame, textvariable=self.replace_string_var, width=30).grid(
            row=2, column=1, sticky=tk.W, padx=(10, 5), pady=5)
        
        # 执行按钮
        ttk.Button(frame, text="开始清理文件名", command=self.clean_filenames,
                  style="Accent.TButton").grid(row=3, column=1, pady=20)
        
        # 配置网格权重
        frame.columnconfigure(1, weight=1)
        
    # 文件夹浏览相关方法
    def browse_rename_folder(self):
        """浏览重命名文件夹"""
        folder = filedialog.askdirectory(title="选择要重命名的文件夹")
        if folder:
            self.rename_folder_var.set(folder)
            
    def browse_clean_folder(self):
        """浏览清理文件夹"""
        folder = filedialog.askdirectory(title="选择要清理文件名的文件夹")
        if folder:
            self.clean_folder_var.set(folder)
            
    def set_today_date(self):
        """设置今天的日期"""
        self.date_var.set(datetime.now().strftime("%Y年%m月%d日"))
        
    # 功能实现方法
    def batch_rename(self):
        """批量重命名文件"""
        folder = self.rename_folder_var.get().strip()
        brand = "品牌"  # 默认品牌名称
        date_str = self.date_var.get().strip()
        start_number_str = self.start_number_var.get().strip()
        
        if not folder:
            messagebox.showerror("错误", "请选择目标文件夹")
            return
            
        if not os.path.exists(folder):
            messagebox.showerror("错误", "目标文件夹不存在")
            return
        
        # 验证编号起始值
        if not start_number_str:
            messagebox.showerror("错误", "请输入编号起始值")
            return
        
        try:
            start_number = int(start_number_str)
            if start_number < 0:
                messagebox.showerror("错误", "编号起始值必须大于等于0")
                return
        except ValueError:
            messagebox.showerror("错误", "编号起始值必须是有效的数字")
            return
            
        # 在新线程中执行
        threading.Thread(target=self._batch_rename_worker, 
                        args=(folder, brand, date_str, start_number), daemon=True).start()
        
    def _batch_rename_worker(self, folder, brand, date_str, start_number):
        """批量重命名的工作线程"""
        try:
            self.status_var.set("正在扫描所有文件...")
            
            # 第一步：收集所有文件信息
            all_files_info = []
            
            # 遍历所有文件夹和子文件夹，收集文件信息
            # os.walk() 会递归遍历所有层级的子文件夹
            for root, dirs, files in os.walk(folder):
                if not files:  # 如果当前文件夹没有文件，跳过
                    continue
                    
                # 获取最后一级文件夹名称（直接包含文件的文件夹名）
                # 例如：/根目录/产品A/颜色1 -> 颜色1
                folder_name = os.path.basename(root)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        # 获取文件的修改时间
                        mtime = os.path.getmtime(file_path)
                        all_files_info.append((file, file_path, mtime, folder_name))
                    except Exception as e:
                        print(f"获取文件时间失败: {file}, 错误: {e}")
                        continue
            
            self.status_var.set("正在按修改时间排序...")
            
            # 第二步：按修改时间全局排序，最早的在前面
            all_files_info.sort(key=lambda x: x[2])
            
            self.status_var.set("正在批量重命名文件...")
            
            # 第三步：全局编号重命名
            renamed_count = 0
            counter = start_number
            
            for file, file_path, mtime, folder_name in all_files_info:
                try:
                    # 获取文件扩展名
                    file_ext = os.path.splitext(file)[1]
                    
                    # 生成新文件名：品牌_文件夹名称_日期_五位编号_副图1
                    new_name = f"{brand}_{folder_name}_{date_str}_{counter:05d}_副图1{file_ext}"
                    new_path = os.path.join(os.path.dirname(file_path), new_name)
                    
                    # 如果新文件名已存在，跳过
                    if os.path.exists(new_path):
                        print(f"文件已存在，跳过: {new_path}")
                        continue
                        
                    # 重命名文件
                    os.rename(file_path, new_path)
                    renamed_count += 1
                    counter += 1
                    
                except Exception as e:
                    print(f"重命名文件失败: {file}, 错误: {e}")
            
            self.status_var.set(f"批量重命名完成，共处理 {renamed_count} 个文件")
            messagebox.showinfo("成功", f"批量重命名完成！\n共重命名 {renamed_count} 个文件\n命名格式: 品牌_文件夹名_日期_五位编号_副图1")
            
        except Exception as e:
            self.status_var.set("重命名失败")
            messagebox.showerror("错误", f"批量重命名失败: {str(e)}")
            
    def clean_filenames(self):
        """清理文件名"""
        folder = self.clean_folder_var.get().strip()
        replace_string = self.replace_string_var.get().strip()
        
        if not folder:
            messagebox.showerror("错误", "请选择目标文件夹")
            return
            
        if not replace_string:
            messagebox.showerror("错误", "请输入要替换的字符串")
            return
            
        if not os.path.exists(folder):
            messagebox.showerror("错误", "目标文件夹不存在")
            return
            
        # 在新线程中执行
        threading.Thread(target=self._clean_filenames_worker, 
                        args=(folder, replace_string), daemon=True).start()
        
    def _clean_filenames_worker(self, folder, replace_string):
        """清理文件名的工作线程"""
        try:
            self.status_var.set("正在清理文件名...")
            
            cleaned_count = 0
            
            # 遍历文件夹和子文件夹
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if replace_string in file:
                        try:
                            old_path = os.path.join(root, file)
                            new_name = file.replace(replace_string, "")
                            new_path = os.path.join(root, new_name)
                            
                            # 如果新文件名已存在，跳过
                            if os.path.exists(new_path):
                                print(f"文件已存在，跳过: {new_path}")
                                continue
                                
                            # 重命名文件
                            os.rename(old_path, new_path)
                            cleaned_count += 1
                            
                        except Exception as e:
                            print(f"清理文件名失败: {file}, 错误: {e}")
            
            self.status_var.set(f"文件名清理完成，共处理 {cleaned_count} 个文件")
            messagebox.showinfo("成功", f"文件名清理完成！\n共清理 {cleaned_count} 个文件")
            
        except Exception as e:
            self.status_var.set("清理失败")
            messagebox.showerror("错误", f"文件名清理失败: {str(e)}")


def main():
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main() 