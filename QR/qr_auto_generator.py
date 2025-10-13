#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR碼自動生產器
功能：
- 批量生成QR碼
- 支持多種內容類型（文字、URL、WiFi、聯絡人、簡訊等）
- 自定義樣式和大小
- 自動命名和組織文件
- 配置文件支持
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask, SquareGradiantColorMask
import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any
import argparse

class QRAutoGenerator:
    def __init__(self, config_file="qr_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.output_dir = self.config.get("output_directory", "qr_codes")
        self.ensure_output_dir()
    
    def load_config(self):
        """載入配置文件"""
        default_config = {
            "output_directory": "qr_codes",
            "default_size": 10,
            "default_border": 4,
            "default_error_correction": "M",
            "default_style": "standard",
            "auto_naming": True,
            "naming_pattern": "{type}_{timestamp}_{index}",
            "image_format": "PNG",
            "styles": {
                "standard": {
                    "module_drawer": "square",
                    "color_mask": "solid",
                    "fill_color": "black",
                    "back_color": "white"
                },
                "rounded": {
                    "module_drawer": "rounded",
                    "color_mask": "radial",
                    "fill_color": "blue",
                    "back_color": "white"
                },
                "gradient": {
                    "module_drawer": "circle",
                    "color_mask": "radial",
                    "fill_color": "purple",
                    "back_color": "white"
                }
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合併默認配置
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"載入配置文件失敗，使用默認配置: {e}")
                return default_config
        else:
            # 創建默認配置文件
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config=None):
        """保存配置文件"""
        if config is None:
            config = self.config
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    
    def ensure_output_dir(self):
        """確保輸出目錄存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_module_drawer(self, drawer_type):
        """獲取模組繪製器"""
        drawers = {
            "square": SquareModuleDrawer(),
            "rounded": RoundedModuleDrawer(),
            "circle": CircleModuleDrawer()
        }
        return drawers.get(drawer_type, SquareModuleDrawer())
    
    def get_color_mask(self, mask_type, fill_color="black", back_color="white"):
        """獲取顏色遮罩"""
        if mask_type == "solid":
            return SolidFillColorMask(back_color=back_color, front_color=fill_color)
        elif mask_type == "radial":
            # 轉換顏色名稱為RGB元組
            color_map = {
                "blue": (70, 130, 180),
                "purple": (128, 0, 128),
                "red": (255, 0, 0),
                "green": (0, 128, 0),
                "black": (0, 0, 0),
                "white": (255, 255, 255)
            }
            center_rgb = color_map.get(fill_color, (0, 0, 0))
            edge_rgb = color_map.get(back_color, (255, 255, 255))
            return RadialGradiantColorMask(
                center_color=center_rgb,
                edge_color=edge_rgb
            )
        elif mask_type == "square":
            return SquareGradiantColorMask(
                center_color=fill_color,
                edge_color=back_color
            )
        else:
            return SolidFillColorMask(back_color=back_color, front_color=fill_color)
    
    def generate_qr(self, data, qr_type="text", style="standard", filename=None, **kwargs):
        """生成單個QR碼"""
        # 獲取樣式配置
        style_config = self.config["styles"].get(style, self.config["styles"]["standard"])
        
        # 創建QR碼
        qr = qrcode.QRCode(
            version=1,
            error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{self.config['default_error_correction']}"),
            box_size=kwargs.get("size", self.config["default_size"]),
            border=kwargs.get("border", self.config["default_border"]),
        )
        
        # 根據類型處理數據
        processed_data = self.process_data(data, qr_type)
        qr.add_data(processed_data)
        qr.make(fit=True)
        
        # 生成圖片
        if style == "standard":
            img = qr.make_image(fill_color=style_config["fill_color"], back_color=style_config["back_color"])
        else:
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=self.get_module_drawer(style_config["module_drawer"]),
                color_mask=self.get_color_mask(style_config["color_mask"], style_config["fill_color"], style_config["back_color"])
            )
        
        # 生成文件名
        if filename is None:
            filename = self.generate_filename(qr_type, **kwargs)
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        
        return {
            "filename": filename,
            "filepath": filepath,
            "type": qr_type,
            "data": data,
            "style": style
        }
    
    def process_data(self, data, qr_type):
        """根據類型處理數據"""
        if qr_type == "url":
            if not data.startswith(("http://", "https://")):
                return f"https://{data}"
            return data
        elif qr_type == "wifi":
            ssid = data.get("ssid", "")
            password = data.get("password", "")
            security = data.get("security", "WPA")
            return f"WIFI:T:{security};S:{ssid};P:{password};H:false;;"
        elif qr_type == "email":
            email = data.get("email", "")
            subject = data.get("subject", "")
            body = data.get("body", "")
            return f"mailto:{email}?subject={subject}&body={body}"
        elif qr_type == "sms":
            phone = data.get("phone", "")
            message = data.get("message", "")
            return f"sms:{phone}:{message}"
        elif qr_type == "phone":
            return f"tel:{data}"
        elif qr_type == "contact":
            # vCard格式
            name = data.get("name", "")
            phone = data.get("phone", "")
            email = data.get("email", "")
            org = data.get("org", "")
            return f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nORG:{org}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
        else:
            return str(data)
    
    def generate_filename(self, qr_type, **kwargs):
        """生成文件名"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        index = kwargs.get("index", "")
        
        if self.config["auto_naming"]:
            pattern = self.config["naming_pattern"]
            filename = pattern.format(
                type=qr_type,
                timestamp=timestamp,
                index=index
            )
        else:
            filename = f"{qr_type}_{timestamp}"
        
        return f"{filename}.{self.config['image_format'].lower()}"
    
    def batch_generate_from_list(self, data_list, qr_type="text", style="standard"):
        """從列表批量生成QR碼"""
        results = []
        for i, data in enumerate(data_list):
            result = self.generate_qr(data, qr_type, style, index=i+1)
            results.append(result)
            print(f"已生成: {result['filename']}")
        return results
    
    def batch_generate_from_csv(self, csv_file, qr_type="text", style="standard"):
        """從CSV文件批量生成QR碼"""
        results = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                data = row.get('data', '')
                if not data:
                    continue
                result = self.generate_qr(data, qr_type, style, index=i+1)
                results.append(result)
                print(f"已生成: {result['filename']}")
        return results
    
    def batch_generate_from_config(self, batch_config):
        """根據配置批量生成QR碼"""
        results = []
        for item in batch_config:
            qr_type = item.get("type", "text")
            data = item.get("data", "")
            style = item.get("style", "standard")
            filename = item.get("filename")
            
            if isinstance(data, dict):
                result = self.generate_qr(data, qr_type, style, filename)
            else:
                result = self.generate_qr(data, qr_type, style, filename)
            
            results.append(result)
            print(f"已生成: {result['filename']}")
        return results

def create_sample_data():
    """創建示例數據"""
    sample_config = {
        "output_directory": "qr_codes",
        "default_size": 15,
        "default_border": 4,
        "default_error_correction": "M",
        "default_style": "standard",
        "auto_naming": True,
        "naming_pattern": "{type}_{timestamp}_{index}",
        "image_format": "PNG",
        "styles": {
            "standard": {
                "module_drawer": "square",
                "color_mask": "solid",
                "fill_color": "black",
                "back_color": "white"
            },
            "rounded": {
                "module_drawer": "rounded",
                "color_mask": "radial",
                "fill_color": "blue",
                "back_color": "white"
            },
            "gradient": {
                "module_drawer": "circle",
                "color_mask": "radial",
                "fill_color": "purple",
                "back_color": "white"
            }
        }
    }
    
    # 保存示例配置
    with open("qr_config.json", 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, indent=4, ensure_ascii=False)
    
    # 創建示例批量配置
    batch_examples = [
        {"type": "text", "data": "Hello World!", "style": "standard"},
        {"type": "url", "data": "https://www.google.com", "style": "rounded"},
        {"type": "wifi", "data": {"ssid": "MyWiFi", "password": "password123", "security": "WPA"}, "style": "gradient"},
        {"type": "email", "data": {"email": "test@example.com", "subject": "Hello", "body": "This is a test email"}, "style": "standard"},
        {"type": "phone", "data": "+1234567890", "style": "rounded"},
        {"type": "contact", "data": {"name": "John Doe", "phone": "+1234567890", "email": "john@example.com", "org": "Example Corp"}, "style": "gradient"}
    ]
    
    with open("batch_examples.json", 'w', encoding='utf-8') as f:
        json.dump(batch_examples, f, indent=4, ensure_ascii=False)
    
    # 創建示例CSV
    csv_data = [
        {"data": "QR Code 1", "type": "text"},
        {"data": "QR Code 2", "type": "text"},
        {"data": "QR Code 3", "type": "text"},
        {"data": "https://github.com", "type": "url"},
        {"data": "https://stackoverflow.com", "type": "url"}
    ]
    
    with open("sample_data.csv", 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['data', 'type']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="QR碼自動生產器")
    parser.add_argument("--mode", choices=["single", "batch", "csv", "config"], default="single", help="生成模式")
    parser.add_argument("--data", help="要編碼的數據")
    parser.add_argument("--type", default="text", help="QR碼類型")
    parser.add_argument("--style", default="standard", help="樣式")
    parser.add_argument("--file", help="批量數據文件")
    parser.add_argument("--create-samples", action="store_true", help="創建示例文件")
    
    args = parser.parse_args()
    
    if args.create_samples:
        create_sample_data()
        print("示例文件已創建：")
        print("- qr_config.json (配置文件)")
        print("- batch_examples.json (批量示例)")
        print("- sample_data.csv (CSV示例)")
        return
    
    generator = QRAutoGenerator()
    
    if args.mode == "single":
        if not args.data:
            print("請提供要編碼的數據 (--data)")
            return
        result = generator.generate_qr(args.data, args.type, args.style)
        print(f"QR碼已生成: {result['filepath']}")
    
    elif args.mode == "batch":
        if not args.file:
            print("請提供批量數據文件 (--file)")
            return
        with open(args.file, 'r', encoding='utf-8') as f:
            batch_config = json.load(f)
        results = generator.batch_generate_from_config(batch_config)
        print(f"批量生成完成，共生成 {len(results)} 個QR碼")
    
    elif args.mode == "csv":
        if not args.file:
            print("請提供CSV文件 (--file)")
            return
        results = generator.batch_generate_from_csv(args.file, args.type, args.style)
        print(f"從CSV批量生成完成，共生成 {len(results)} 個QR碼")

if __name__ == "__main__":
    main()
