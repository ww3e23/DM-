#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR碼自動生產器 - 快速啟動腳本
提供簡單的菜單選擇界面
"""

import os
import sys
import subprocess

def check_dependencies():
    """檢查依賴項"""
    try:
        import qrcode
        import tkinter
        return True
    except ImportError as e:
        print(f"缺少依賴項: {e}")
        print("請運行: pip install -r requirements.txt")
        return False

def create_sample_files():
    """創建示例文件"""
    print("正在創建示例文件...")
    try:
        subprocess.run([sys.executable, "qr_auto_generator.py", "--create-samples"], check=True)
        print("示例文件創建完成！")
    except subprocess.CalledProcessError:
        print("創建示例文件失敗")

def run_gui():
    """運行圖形界面"""
    print("啟動圖形界面...")
    try:
        subprocess.run([sys.executable, "qr_gui.py"], check=True)
    except subprocess.CalledProcessError:
        print("啟動圖形界面失敗")

def run_cli():
    """運行命令行版本"""
    print("啟動命令行版本...")
    print("使用 'python qr_auto_generator.py --help' 查看幫助")
    try:
        subprocess.run([sys.executable, "qr_auto_generator.py", "--help"], check=True)
    except subprocess.CalledProcessError:
        print("啟動命令行版本失敗")

def show_menu():
    """顯示主菜單"""
    while True:
        print("\n" + "="*50)
        print("QR碼自動生產器")
        print("="*50)
        print("1. 啟動圖形界面 (推薦)")
        print("2. 啟動命令行版本")
        print("3. 創建示例文件")
        print("4. 查看使用說明")
        print("5. 退出")
        print("="*50)
        
        choice = input("請選擇 (1-5): ").strip()
        
        if choice == "1":
            if check_dependencies():
                run_gui()
            else:
                input("按Enter鍵繼續...")
        elif choice == "2":
            if check_dependencies():
                run_cli()
            else:
                input("按Enter鍵繼續...")
        elif choice == "3":
            create_sample_files()
            input("按Enter鍵繼續...")
        elif choice == "4":
            show_help()
        elif choice == "5":
            print("再見！")
            break
        else:
            print("無效選擇，請重新輸入")

def show_help():
    """顯示幫助信息"""
    print("\n" + "="*50)
    print("使用說明")
    print("="*50)
    print("1. 圖形界面版本 (qr_gui.py)")
    print("   - 提供友好的GUI界面")
    print("   - 支持單個和批量生成")
    print("   - 支持多種QR碼類型")
    print("   - 支持文件載入和保存")
    print()
    print("2. 命令行版本 (qr_auto_generator.py)")
    print("   - 支持腳本化批量生成")
    print("   - 支持配置文件")
    print("   - 支持CSV批量處理")
    print()
    print("3. 支持的QR碼類型:")
    print("   - text: 文字")
    print("   - url: 網址")
    print("   - wifi: WiFi配置")
    print("   - email: 郵件")
    print("   - sms: 簡訊")
    print("   - phone: 電話")
    print("   - contact: 聯絡人")
    print()
    print("4. 支持的樣式:")
    print("   - standard: 標準樣式")
    print("   - rounded: 圓角樣式")
    print("   - gradient: 漸變樣式")
    print()
    print("5. 輸出文件:")
    print("   - 保存在 qr_codes 文件夾")
    print("   - PNG格式")
    print("   - 自動命名")
    print("="*50)
    input("按Enter鍵返回主菜單...")

def main():
    """主函數"""
    print("歡迎使用QR碼自動生產器！")
    
    # 檢查是否在正確的目錄
    required_files = ["qr_auto_generator.py", "qr_gui.py", "requirements.txt"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"錯誤: 缺少以下文件: {', '.join(missing_files)}")
        print("請確保在正確的目錄中運行此腳本")
        return
    
    show_menu()

if __name__ == "__main__":
    main()
