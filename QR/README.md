# QR碼自動生產器

一個功能強大的QR碼自動生成工具，支持單個生成、批量生成、多種內容類型和自定義樣式。

## 功能特色

- 🚀 **多種生成模式**: 單個生成、批量生成、CSV批量、配置文件批量
- 🎨 **多種樣式**: 標準、圓角、漸變等樣式
- 📱 **多種內容類型**: 文字、URL、WiFi、郵件、簡訊、電話、聯絡人
- 🖥️ **圖形界面**: 友好的GUI界面，操作簡單
- ⚙️ **配置文件**: 支持自定義配置和批量配置
- 📁 **自動組織**: 自動命名和文件組織

## 安裝要求

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 圖形界面版本 (推薦)

```bash
python qr_gui.py
```

圖形界面提供以下功能：
- 單個QR碼生成
- 批量文本生成
- 從CSV/JSON文件載入數據
- 配置管理
- 輸出文件夾管理

### 2. 命令行版本

#### 創建示例文件
```bash
python qr_auto_generator.py --create-samples
```

#### 單個生成
```bash
python qr_auto_generator.py --mode single --data "Hello World!" --type text --style standard
```

#### 批量生成
```bash
python qr_auto_generator.py --mode batch --file batch_examples.json
```

#### CSV批量生成
```bash
python qr_auto_generator.py --mode csv --file sample_data.csv --type text --style rounded
```

### 3. 程序化使用

```python
from qr_auto_generator import QRAutoGenerator

# 創建生成器
generator = QRAutoGenerator()

# 生成單個QR碼
result = generator.generate_qr("Hello World!", "text", "standard")
print(f"QR碼已生成: {result['filepath']}")

# 批量生成
data_list = ["QR Code 1", "QR Code 2", "QR Code 3"]
results = generator.batch_generate_from_list(data_list, "text", "rounded")
print(f"批量生成完成，共 {len(results)} 個QR碼")
```

## 支持的QR碼類型

### 1. 文字 (text)
```python
generator.generate_qr("Hello World!", "text")
```

### 2. URL (url)
```python
generator.generate_qr("https://www.google.com", "url")
```

### 3. WiFi (wifi)
```python
wifi_data = {
    "ssid": "MyWiFi",
    "password": "password123",
    "security": "WPA"
}
generator.generate_qr(wifi_data, "wifi")
```

### 4. 郵件 (email)
```python
email_data = {
    "email": "test@example.com",
    "subject": "Hello",
    "body": "This is a test email"
}
generator.generate_qr(email_data, "email")
```

### 5. 簡訊 (sms)
```python
sms_data = {
    "phone": "+1234567890",
    "message": "Hello from QR code!"
}
generator.generate_qr(sms_data, "sms")
```

### 6. 電話 (phone)
```python
generator.generate_qr("+1234567890", "phone")
```

### 7. 聯絡人 (contact)
```python
contact_data = {
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john@example.com",
    "org": "Example Corp"
}
generator.generate_qr(contact_data, "contact")
```

## 樣式選項

### 1. 標準樣式 (standard)
- 方形模組
- 單色填充
- 黑白配色

### 2. 圓角樣式 (rounded)
- 圓角模組
- 徑向漸變
- 藍色配色

### 3. 漸變樣式 (gradient)
- 圓形模組
- 徑向漸變
- 紫色配色

## 配置文件

### 主配置文件 (qr_config.json)
```json
{
    "output_directory": "qr_codes",
    "default_size": 15,
    "default_border": 4,
    "default_error_correction": "M",
    "default_style": "standard",
    "auto_naming": true,
    "naming_pattern": "{type}_{timestamp}_{index}",
    "image_format": "PNG",
    "styles": {
        "standard": {
            "module_drawer": "square",
            "color_mask": "solid",
            "fill_color": "black",
            "back_color": "white"
        }
    }
}
```

### 批量配置文件 (batch_examples.json)
```json
[
    {
        "type": "text",
        "data": "Hello World!",
        "style": "standard"
    },
    {
        "type": "url",
        "data": "https://www.google.com",
        "style": "rounded"
    }
]
```

### CSV文件格式 (sample_data.csv)
```csv
data,type
Hello World!,text
https://www.google.com,url
QR Code 3,text
```

## 圖形界面使用指南

### 單個QR碼生成
1. 選擇QR碼類型（文字、URL、WiFi等）
2. 選擇樣式（標準、圓角、漸變）
3. 輸入數據
4. 點擊"生成QR碼"

### 批量生成
1. 在批量數據區域輸入多行數據
2. 選擇QR碼類型和樣式
3. 點擊"批量生成"

### 文件操作
- **從CSV載入**: 載入CSV文件中的數據
- **從JSON載入**: 載入JSON配置文件
- **保存配置**: 保存當前配置
- **打開輸出文件夾**: 打開生成的QR碼文件夾

## 數據格式說明

### WiFi格式
```
SSID:Password
```

### 郵件格式
```
email@domain.com:Subject:Body
```

### 簡訊格式
```
phone:message
```

### 聯絡人格式
```
Name:Phone:Email:Organization
```

## 輸出文件

- 所有生成的QR碼保存在 `qr_codes` 文件夾中
- 文件名格式: `{type}_{timestamp}_{index}.png`
- 支持PNG格式輸出

## 錯誤處理

程序包含完整的錯誤處理機制：
- 輸入驗證
- 文件操作錯誤處理
- 配置錯誤處理
- 用戶友好的錯誤提示

## 擴展功能

### 自定義樣式
可以在配置文件中添加自定義樣式：
```json
{
    "styles": {
        "custom": {
            "module_drawer": "rounded",
            "color_mask": "radial",
            "fill_color": "red",
            "back_color": "yellow"
        }
    }
}
```

### 自定義命名模式
```json
{
    "naming_pattern": "QR_{type}_{date}_{time}_{index}"
}
```

## 故障排除

### 常見問題

1. **模組未安裝**
   ```bash
   pip install -r requirements.txt
   ```

2. **權限錯誤**
   - 確保對輸出目錄有寫入權限
   - 在Windows上可能需要管理員權限

3. **中文顯示問題**
   - 確保終端支持UTF-8編碼
   - 在Windows上可能需要設置代碼頁

4. **GUI無法啟動**
   - 確保安裝了tkinter
   - 在Linux上可能需要安裝python3-tk

## 更新日誌

### v1.0.0
- 初始版本發布
- 支持基本QR碼生成
- 圖形界面
- 批量生成功能
- 多種內容類型支持

## 授權

MIT License

## 貢獻

歡迎提交Issue和Pull Request來改進這個項目！
