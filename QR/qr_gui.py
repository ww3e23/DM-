#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR碼自動生產器 - 圖形界面版本
提供友好的GUI界面來生成和管理QR碼
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from datetime import datetime
from qr_auto_generator import QRAutoGenerator

class QRGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QR碼自動生產器")
        self.root.geometry("800x600")
        
        # 初始化生成器
        self.generator = QRAutoGenerator()
        
        # 創建界面
        self.create_widgets()
        
        # 載入示例數據
        self.load_sample_data()
    
    def create_widgets(self):
        """創建界面組件"""
        # 創建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 標題
        title_label = ttk.Label(main_frame, text="QR碼自動生產器", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 單個QR碼生成區域
        single_frame = ttk.LabelFrame(main_frame, text="單個QR碼生成", padding="10")
        single_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        single_frame.columnconfigure(1, weight=1)
        
        # QR碼類型
        ttk.Label(single_frame, text="類型:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.qr_type_var = tk.StringVar(value="text")
        type_combo = ttk.Combobox(single_frame, textvariable=self.qr_type_var, 
                                 values=["text", "url", "wifi", "email", "sms", "phone", "contact"])
        type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        # 樣式
        ttk.Label(single_frame, text="樣式:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0), pady=2)
        self.style_var = tk.StringVar(value="standard")
        style_combo = ttk.Combobox(single_frame, textvariable=self.style_var,
                                  values=["standard", "rounded", "gradient"])
        style_combo.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        # 數據輸入
        ttk.Label(single_frame, text="數據:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.data_entry = ttk.Entry(single_frame)
        self.data_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        # 生成按鈕
        generate_btn = ttk.Button(single_frame, text="生成QR碼", command=self.generate_single)
        generate_btn.grid(row=1, column=3, padx=(5, 0), pady=2)
        
        # 批量生成區域
        batch_frame = ttk.LabelFrame(main_frame, text="批量生成", padding="10")
        batch_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        batch_frame.columnconfigure(1, weight=1)
        
        # 批量數據輸入
        ttk.Label(batch_frame, text="批量數據:").grid(row=0, column=0, sticky=(tk.W, tk.N), pady=2)
        self.batch_text = scrolledtext.ScrolledText(batch_frame, height=8, width=50)
        self.batch_text.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        # 批量生成按鈕
        batch_btn = ttk.Button(batch_frame, text="批量生成", command=self.generate_batch)
        batch_btn.grid(row=0, column=3, padx=(5, 0), pady=2)
        
        # 文件操作區域
        file_frame = ttk.LabelFrame(main_frame, text="文件操作", padding="10")
        file_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 載入CSV按鈕
        csv_btn = ttk.Button(file_frame, text="從CSV載入", command=self.load_csv)
        csv_btn.grid(row=0, column=0, padx=(0, 5))
        
        # 載入JSON按鈕
        json_btn = ttk.Button(file_frame, text="從JSON載入", command=self.load_json)
        json_btn.grid(row=0, column=1, padx=5)
        
        # 保存配置按鈕
        save_btn = ttk.Button(file_frame, text="保存配置", command=self.save_config)
        save_btn.grid(row=0, column=2, padx=5)
        
        # 打開輸出文件夾按鈕
        open_btn = ttk.Button(file_frame, text="打開輸出文件夾", command=self.open_output_folder)
        open_btn.grid(row=0, column=3, padx=5)
        
        # 狀態區域
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        # 狀態標籤
        self.status_var = tk.StringVar(value="就緒")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # 進度條
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
    
    def load_sample_data(self):
        """載入示例數據"""
        sample_data = """Hello World!
https://www.google.com
https://github.com
https://stackoverflow.com
我的網站
聯絡資訊"""
        self.batch_text.insert(tk.END, sample_data)
    
    def generate_single(self):
        """生成單個QR碼"""
        data = self.data_entry.get().strip()
        if not data:
            messagebox.showerror("錯誤", "請輸入要編碼的數據")
            return
        
        try:
            self.status_var.set("生成中...")
            self.progress.start()
            self.root.update()
            
            qr_type = self.qr_type_var.get()
            style = self.style_var.get()
            
            # 根據類型處理數據
            processed_data = self.process_single_data(data, qr_type)
            
            result = self.generator.generate_qr(processed_data, qr_type, style)
            
            self.progress.stop()
            self.status_var.set("生成完成")
            
            messagebox.showinfo("成功", f"QR碼已生成:\n{result['filepath']}")
            
        except Exception as e:
            self.progress.stop()
            self.status_var.set("生成失敗")
            messagebox.showerror("錯誤", f"生成失敗: {str(e)}")
    
    def process_single_data(self, data, qr_type):
        """處理單個數據"""
        if qr_type == "wifi":
            # 簡單的WiFi格式: SSID:Password
            if ":" in data:
                ssid, password = data.split(":", 1)
                return {"ssid": ssid.strip(), "password": password.strip(), "security": "WPA"}
            else:
                return {"ssid": data, "password": "", "security": "WPA"}
        elif qr_type == "email":
            # 簡單的郵件格式: email@domain.com:Subject:Body
            parts = data.split(":", 2)
            return {
                "email": parts[0].strip(),
                "subject": parts[1].strip() if len(parts) > 1 else "",
                "body": parts[2].strip() if len(parts) > 2 else ""
            }
        elif qr_type == "sms":
            # 簡單的簡訊格式: phone:message
            if ":" in data:
                phone, message = data.split(":", 1)
                return {"phone": phone.strip(), "message": message.strip()}
            else:
                return {"phone": data, "message": ""}
        elif qr_type == "contact":
            # 簡單的聯絡人格式: Name:Phone:Email:Organization
            parts = data.split(":")
            return {
                "name": parts[0].strip() if len(parts) > 0 else "",
                "phone": parts[1].strip() if len(parts) > 1 else "",
                "email": parts[2].strip() if len(parts) > 2 else "",
                "org": parts[3].strip() if len(parts) > 3 else ""
            }
        else:
            return data
    
    def generate_batch(self):
        """批量生成QR碼"""
        data_text = self.batch_text.get("1.0", tk.END).strip()
        if not data_text:
            messagebox.showerror("錯誤", "請輸入批量數據")
            return
        
        try:
            self.status_var.set("批量生成中...")
            self.progress.start()
            self.root.update()
            
            # 分割數據
            data_list = [line.strip() for line in data_text.split('\n') if line.strip()]
            
            qr_type = self.qr_type_var.get()
            style = self.style_var.get()
            
            results = []
            for i, data in enumerate(data_list):
                processed_data = self.process_single_data(data, qr_type)
                result = self.generator.generate_qr(processed_data, qr_type, style, index=i+1)
                results.append(result)
            
            self.progress.stop()
            self.status_var.set("批量生成完成")
            
            messagebox.showinfo("成功", f"批量生成完成，共生成 {len(results)} 個QR碼")
            
        except Exception as e:
            self.progress.stop()
            self.status_var.set("批量生成失敗")
            messagebox.showerror("錯誤", f"批量生成失敗: {str(e)}")
    
    def load_csv(self):
        """從CSV文件載入數據"""
        file_path = filedialog.askopenfilename(
            title="選擇CSV文件",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                import csv
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data_list = []
                    for row in reader:
                        data = row.get('data', '')
                        if data:
                            data_list.append(data)
                
                # 更新批量文本區域
                self.batch_text.delete("1.0", tk.END)
                self.batch_text.insert("1.0", '\n'.join(data_list))
                
                messagebox.showinfo("成功", f"已載入 {len(data_list)} 條數據")
                
            except Exception as e:
                messagebox.showerror("錯誤", f"載入CSV失敗: {str(e)}")
    
    def load_json(self):
        """從JSON文件載入配置"""
        file_path = filedialog.askopenfilename(
            title="選擇JSON文件",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 更新生成器配置
                self.generator.config.update(config)
                self.generator.save_config()
                
                messagebox.showinfo("成功", "配置已載入")
                
            except Exception as e:
                messagebox.showerror("錯誤", f"載入JSON失敗: {str(e)}")
    
    def save_config(self):
        """保存當前配置"""
        try:
            self.generator.save_config()
            messagebox.showinfo("成功", "配置已保存")
        except Exception as e:
            messagebox.showerror("錯誤", f"保存配置失敗: {str(e)}")
    
    def open_output_folder(self):
        """打開輸出文件夾"""
        try:
            import subprocess
            import platform
            
            output_path = os.path.abspath(self.generator.output_dir)
            
            if platform.system() == "Windows":
                os.startfile(output_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", output_path])
            else:  # Linux
                subprocess.run(["xdg-open", output_path])
                
        except Exception as e:
            messagebox.showerror("錯誤", f"無法打開文件夾: {str(e)}")

def main():
    """主函數"""
    root = tk.Tk()
    app = QRGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
