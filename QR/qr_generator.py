#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR碼生成器
可以生成各種類型的QR碼，包括文字、URL、WiFi配置等
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import os
from datetime import datetime

def generate_text_qr(text, filename=None):
    """生成文字QR碼"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"text_qr_{timestamp}.png"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    # 創建QR碼圖片
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"文字QR碼已生成: {filename}")
    return filename

def generate_url_qr(url, filename=None):
    """生成URL QR碼"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"url_qr_{timestamp}.png"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"URL QR碼已生成: {filename}")
    return filename

def generate_wifi_qr(ssid, password, security="WPA", filename=None):
    """生成WiFi配置QR碼"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wifi_qr_{timestamp}.png"
    
    wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};H:false;;"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_string)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"WiFi QR碼已生成: {filename}")
    return filename

def generate_styled_qr(text, filename=None):
    """生成帶樣式的QR碼"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"styled_qr_{timestamp}.png"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    # 創建帶樣式的QR碼
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(
            center_color=(70, 130, 180),  # 鋼藍色
            edge_color=(25, 25, 112)      # 午夜藍
        )
    )
    img.save(filename)
    print(f"樣式QR碼已生成: {filename}")
    return filename

def main():
    """主函數 - 生成示例QR碼"""
    print("QR碼生成器")
    print("=" * 50)
    
    # 生成示例QR碼
    examples = [
        ("Hello World!", "text"),
        ("https://www.google.com", "url"),
        ("MyWiFi", "wifi", "MyPassword123"),
        ("樣式QR碼測試", "styled")
    ]
    
    for example in examples:
        if example[1] == "text":
            generate_text_qr(example[0])
        elif example[1] == "url":
            generate_url_qr(example[0])
        elif example[1] == "wifi":
            generate_wifi_qr(example[0], example[2])
        elif example[1] == "styled":
            generate_styled_qr(example[0])
    
    print("\n所有示例QR碼已生成完成！")
    print("您可以使用以下函數來生成自定義QR碼：")
    print("- generate_text_qr('您的文字')")
    print("- generate_url_qr('https://example.com')")
    print("- generate_wifi_qr('WiFi名稱', '密碼')")
    print("- generate_styled_qr('您的文字')")

if __name__ == "__main__":
    main()
