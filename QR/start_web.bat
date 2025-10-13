@echo off
chcp 65001 >nul
title QR碼自動生產器 - 網頁版

echo 正在啟動QR碼自動生產器網頁版...
echo.

REM 檢查Python是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤: 未找到Python，請先安裝Python
    pause
    exit /b 1
)

REM 啟動網頁版
python start_web.py

pause
