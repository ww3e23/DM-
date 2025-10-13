#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR碼自動生產器 - Flask網頁版後端
提供API接口和文件管理功能
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import qrcode
import io
import base64
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'generated_qr'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'json'}

# 確保文件夾存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_qr_code(data, qr_type="text", style="standard", size=256):
    """生成QR碼"""
    # 根據類型處理數據
    processed_data = process_data(data, qr_type)
    
    # 創建QR碼
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(processed_data)
    qr.make(fit=True)
    
    # 生成圖片
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 調整大小
    img = img.resize((size, size))
    
    return img

def process_data(data, qr_type):
    """根據類型處理數據"""
    if qr_type == "url":
        if not data.startswith(("http://", "https://")):
            return f"https://{data}"
        return data
    elif qr_type == "wifi":
        # 處理WiFi數據
        if isinstance(data, dict):
            ssid = data.get("ssid", "")
            password = data.get("password", "")
            security = data.get("security", "WPA")
            return f"WIFI:T:{security};S:{ssid};P:{password};H:false;;"
        return data
    elif qr_type == "email":
        if isinstance(data, dict):
            email = data.get("email", "")
            subject = data.get("subject", "")
            body = data.get("body", "")
            return f"mailto:{email}?subject={subject}&body={body}"
        return data
    elif qr_type == "sms":
        if isinstance(data, dict):
            phone = data.get("phone", "")
            message = data.get("message", "")
            return f"sms:{phone}:{message}"
        return data
    elif qr_type == "phone":
        return f"tel:{data}"
    elif qr_type == "contact":
        if isinstance(data, dict):
            name = data.get("name", "")
            phone = data.get("phone", "")
            email = data.get("email", "")
            org = data.get("org", "")
            return f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nORG:{org}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
        return data
    else:
        return str(data)

@app.route('/')
def index():
    """主頁"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API: 生成單個QR碼"""
    try:
        data = request.get_json()
        
        qr_data = data.get('data', '')
        qr_type = data.get('type', 'text')
        style = data.get('style', 'standard')
        size = data.get('size', 256)
        
        if not qr_data:
            return jsonify({'error': '請提供要編碼的數據'}), 400
        
        # 生成QR碼
        img = generate_qr_code(qr_data, qr_type, style, size)
        
        # 轉換為base64
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'data': img_base64,
            'filename': f"qrcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def api_batch():
    """API: 批量生成QR碼"""
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({'error': '請提供批量數據'}), 400
        
        results = []
        for i, item in enumerate(items):
            qr_data = item.get('data', '')
            qr_type = item.get('type', 'text')
            style = item.get('style', 'standard')
            size = item.get('size', 256)
            
            if not qr_data:
                continue
            
            # 生成QR碼
            img = generate_qr_code(qr_data, qr_type, style, size)
            
            # 保存文件
            filename = f"qrcode_batch_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            img.save(filepath)
            
            results.append({
                'filename': filename,
                'filepath': filepath,
                'data': qr_data,
                'type': qr_type
            })
        
        return jsonify({
            'success': True,
            'count': len(results),
            'files': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API: 上傳文件並解析"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '沒有選擇文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '沒有選擇文件'}), 400
        
        if file and allowed_file(file.filename):
            filename = f"{uuid.uuid4()}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # 解析文件內容
            items = []
            if file.filename.endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            items.append({'data': line, 'type': 'text'})
            elif file.filename.endswith('.csv'):
                import csv
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('data'):
                            items.append({
                                'data': row['data'],
                                'type': row.get('type', 'text')
                            })
            elif file.filename.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        items = data
                    else:
                        items = [data]
            
            # 清理上傳的文件
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'items': items,
                'count': len(items)
            })
        
        return jsonify({'error': '不支持的文件類型'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def api_download(filename):
    """API: 下載生成的QR碼文件"""
    try:
        return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': '文件不存在'}), 404

@app.route('/api/files')
def api_files():
    """API: 獲取已生成的文件列表"""
    try:
        files = []
        for filename in os.listdir(OUTPUT_FOLDER):
            if filename.endswith('.png'):
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                stat = os.stat(filepath)
                files.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
        
        # 按創建時間排序
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete/<filename>', methods=['DELETE'])
def api_delete(filename):
    """API: 刪除文件"""
    try:
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True})
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['DELETE'])
def api_clear():
    """API: 清空所有生成的文件"""
    try:
        for filename in os.listdir(OUTPUT_FOLDER):
            if filename.endswith('.png'):
                os.remove(os.path.join(OUTPUT_FOLDER, filename))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """健康檢查"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 QR碼自動生產器 - 網頁版")
    print("=" * 50)
    print("訪問地址: http://localhost:5000")
    print("API文檔: http://localhost:5000/health")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
