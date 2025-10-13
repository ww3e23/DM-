@echo off
echo 启动整合平台...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查是否在正确的目录
if not exist "app.py" (
    echo 错误: 请在platform目录下运行此脚本
    pause
    exit /b 1
)

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt

REM 启动应用
echo.
echo 启动Flask应用...
echo 访问地址: http://localhost:5000
echo 默认管理员: admin / admin123
echo.
echo 按 Ctrl+C 停止服务
echo.

python app.py

pause
