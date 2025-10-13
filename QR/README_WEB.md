# QR碼自動生產器 - 網頁版

一個功能強大的網頁版QR碼生成工具，支持多種內容類型、批量生成和文件上傳。

## 🌟 功能特色

- 🖥️ **網頁界面**: 現代化的響應式設計，支持手機和電腦
- 🎨 **多種樣式**: 標準、圓角、漸變等視覺樣式
- 📱 **多種類型**: 文字、URL、WiFi、郵件、簡訊、電話、聯絡人
- 📦 **批量生成**: 支持批量處理和文件上傳
- 💾 **多格式下載**: PNG和SVG格式下載
- 🔧 **API接口**: 完整的REST API支持

## 🚀 快速開始

### 方法1: 自動啟動（推薦）
```bash
# Windows用戶
雙擊 start_web.bat

# 或使用Python
python start_web.py
```

### 方法2: 手動啟動
```bash
# 安裝依賴
pip install flask qrcode[pil] Pillow

# 啟動服務器
python app.py
```

然後在瀏覽器中訪問: http://localhost:5000

## 📱 使用方法

### 單個QR碼生成
1. 選擇QR碼類型（文字、URL、WiFi等）
2. 選擇樣式（標準、圓角、漸變）
3. 輸入相應的數據
4. 點擊"生成QR碼"
5. 下載PNG或SVG格式

### 批量生成
1. **手動添加**: 在批量輸入框中輸入內容，點擊"添加到列表"
2. **文件上傳**: 上傳TXT、CSV或JSON文件
3. 點擊"批量生成所有QR碼"
4. 系統會自動下載所有生成的QR碼

## 📁 支持的文件格式

### TXT文件
```
Hello World!
https://www.google.com
我的網站
聯絡資訊
```

### CSV文件
```csv
data,type
Hello World!,text
https://www.google.com,url
QR Code 3,text
```

### JSON文件
```json
[
    {
        "data": "Hello World!",
        "type": "text",
        "style": "standard"
    },
    {
        "data": "https://www.google.com",
        "type": "url",
        "style": "rounded"
    }
]
```

## 🔧 API接口

### 生成單個QR碼
```bash
POST /api/generate
Content-Type: application/json

{
    "data": "Hello World!",
    "type": "text",
    "style": "standard",
    "size": 256
}
```

### 批量生成
```bash
POST /api/batch
Content-Type: application/json

{
    "items": [
        {
            "data": "Hello World!",
            "type": "text",
            "style": "standard"
        }
    ]
}
```

### 文件上傳
```bash
POST /api/upload
Content-Type: multipart/form-data

file: [文件內容]
```

### 下載文件
```bash
GET /api/download/{filename}
```

### 獲取文件列表
```bash
GET /api/files
```

### 健康檢查
```bash
GET /health
```

## 🎨 QR碼類型說明

### 文字 (text)
直接編碼文字內容

### 網址 (url)
編碼網址，掃描後直接跳轉

### WiFi (wifi)
編碼WiFi配置信息
- WiFi名稱
- 密碼
- 安全類型 (WPA/WEP/無密碼)

### 郵件 (email)
編碼郵件信息
- 郵件地址
- 主題
- 內容

### 簡訊 (sms)
編碼簡訊信息
- 電話號碼
- 簡訊內容

### 電話 (phone)
編碼電話號碼，掃描後直接撥打

### 聯絡人 (contact)
編碼聯絡人信息 (vCard格式)
- 姓名
- 電話
- 郵件
- 組織

## 🎭 樣式選項

### 標準樣式 (standard)
- 方形模組
- 黑白配色
- 經典外觀

### 圓角樣式 (rounded)
- 圓角模組
- 藍色配色
- 現代外觀

### 漸變樣式 (gradient)
- 圓形模組
- 紫色配色
- 藝術外觀

## 📱 響應式設計

- 支持桌面電腦、平板和手機
- 自適應布局
- 觸摸友好的界面

## 🔒 安全性

- 所有數據在本地處理
- 不存儲用戶隱私信息
- 支持HTTPS（生產環境）

## 🛠️ 技術架構

### 前端
- HTML5 + CSS3
- JavaScript (ES6+)
- 響應式設計
- Fetch API

### 後端
- Python Flask
- QRCode庫
- RESTful API
- 文件處理

### 依賴項
```
Flask==2.3.3
qrcode[pil]==7.4.2
Pillow==10.0.1
```

## 🚀 部署

### 本地開發
```bash
python app.py
```

### 生產環境
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 或使用uWSGI
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app
```

## 📝 更新日誌

### v1.0.0
- 初始版本發布
- 支持基本QR碼生成
- 網頁界面
- 批量生成功能
- API接口
- 文件上傳支持

## 🤝 貢獻

歡迎提交Issue和Pull Request來改進這個項目！

## 📄 授權

MIT License

## 🆘 故障排除

### 常見問題

1. **端口被佔用**
   - 修改app.py中的端口號
   - 或使用其他端口: `python app.py --port 8080`

2. **依賴項安裝失敗**
   - 確保Python版本 >= 3.7
   - 使用虛擬環境: `python -m venv venv && venv\Scripts\activate`

3. **文件上傳失敗**
   - 檢查文件格式是否支持
   - 確保文件大小不超過限制

4. **QR碼生成失敗**
   - 檢查輸入數據是否有效
   - 確保數據長度不超過QR碼限制

## 📞 支持

如有問題，請提交Issue或聯繫開發者。
