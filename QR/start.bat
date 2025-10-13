@echo off
chcp 65001 >nul
title QR碼自動生產器

echo 正在啟動QR碼自動生產器...
echo.

REM 檢查Python是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤: 未找到Python，請先安裝Python
    pause
    exit /b 1
)

REM 檢查依賴項
python -c "import qrcode, tkinter" >nul 2>&1
if errorlevel 1 (
    echo 正在安裝依賴項...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 安裝依賴項失敗，請手動運行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM 啟動程序
python start.py

pause
