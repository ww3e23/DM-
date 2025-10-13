#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR碼自動生產器 - 網頁版啟動腳本
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading

def check_dependencies():
    """檢查依賴項"""
    try:
        import flask
        import qrcode
        return True
    except ImportError as e:
        print(f"缺少依賴項: {e}")
        print("正在安裝依賴項...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask", "qrcode[pil]", "Pillow"], check=True)
            print("依賴項安裝完成！")
            return True
        except subprocess.CalledProcessError:
            print("依賴項安裝失敗，請手動運行:")
            print("pip install flask qrcode[pil] Pillow")
            return False

def open_browser():
    """延遲打開瀏覽器"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def main():
    """主函數"""
    print("🚀 QR碼自動生產器 - 網頁版")
    print("=" * 50)
    
    # 檢查依賴項
    if not check_dependencies():
        input("按Enter鍵退出...")
        return
    
    # 檢查必要文件
    required_files = ["app.py", "templates/index.html"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"錯誤: 缺少以下文件: {', '.join(missing_files)}")
        input("按Enter鍵退出...")
        return
    
    print("正在啟動網頁服務器...")
    print("訪問地址: http://localhost:5000")
    print("按 Ctrl+C 停止服務器")
    print("=" * 50)
    
    # 在後台線程中打開瀏覽器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # 啟動Flask應用
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n服務器已停止")
    except subprocess.CalledProcessError as e:
        print(f"啟動失敗: {e}")
        input("按Enter鍵退出...")

if __name__ == "__main__":
    main()
