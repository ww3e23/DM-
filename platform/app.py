#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合平台 - 主应用
整合DM生产器和QR生成器，提供用户管理和后台功能
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
import uuid
import qrcode
import io
import base64
from functools import wraps
from config import config

app = Flask(__name__)

# 配置
config_name = os.environ.get('FLASK_ENV') or 'default'
app.config.from_object(config[config_name])

# 初始化扩展
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 数据库模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # 用户福利和方案
    plan_type = db.Column(db.String(50), default='free')  # free, basic, premium, enterprise
    dm_usage_count = db.Column(db.Integer, default=0)
    qr_usage_count = db.Column(db.Integer, default=0)
    dm_monthly_limit = db.Column(db.Integer, default=10)  # 每月DM生成限制
    qr_monthly_limit = db.Column(db.Integer, default=50)  # 每月QR生成限制
    plan_expires_at = db.Column(db.DateTime)
    
    # 关联记录
    dm_records = db.relationship('DMRecord', backref='user', lazy=True)
    qr_records = db.relationship('QRRecord', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

class DMRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    template_name = db.Column(db.String(100), nullable=False)
    content_data = db.Column(db.Text)  # JSON格式存储内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(200))

class QRRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    qr_type = db.Column(db.String(50), nullable=False)
    content_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(200))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

class SystemConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 权限装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated_function

# 使用限制检查装饰器
def check_usage_limit(service_type):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': '请先登录'}), 401
            
            # 检查使用限制
            if service_type == 'dm':
                if current_user.dm_usage_count >= current_user.dm_monthly_limit:
                    return jsonify({'error': f'本月DM生成次数已达上限 ({current_user.dm_monthly_limit})'}), 429
            elif service_type == 'qr':
                if current_user.qr_usage_count >= current_user.qr_monthly_limit:
                    return jsonify({'error': f'本月QR生成次数已达上限 ({current_user.qr_monthly_limit})'}), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 路由
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        else:
            return jsonify({'error': '用户名或密码错误'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'error': '用户名已存在'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': '邮箱已存在'}), 400
        
        # 创建新用户
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'redirect': url_for('dashboard')})
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/dm-generator')
@login_required
def dm_generator():
    return render_template('dm_generator.html')

@app.route('/qr-generator')
@login_required
def qr_generator():
    return render_template('qr_generator.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')

# API路由
@app.route('/api/user/stats')
@login_required
def user_stats():
    """获取用户统计信息"""
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'plan_type': current_user.plan_type,
        'dm_usage_count': current_user.dm_usage_count,
        'qr_usage_count': current_user.qr_usage_count,
        'dm_monthly_limit': current_user.dm_monthly_limit,
        'qr_monthly_limit': current_user.qr_monthly_limit,
        'plan_expires_at': current_user.plan_expires_at.isoformat() if current_user.plan_expires_at else None
    })

@app.route('/api/dm/generate', methods=['POST'])
@login_required
@check_usage_limit('dm')
def generate_dm():
    """生成DM"""
    try:
        data = request.get_json()
        
        # 这里整合DM生成逻辑
        # 暂时返回成功，实际需要调用DM生成器
        
        # 记录使用次数
        current_user.dm_usage_count += 1
        db.session.commit()
        
        # 保存记录
        record = DMRecord(
            user_id=current_user.id,
            template_name=data.get('template', 'default'),
            content_data=json.dumps(data)
        )
        db.session.add(record)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'DM生成成功'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/qr/generate', methods=['POST'])
@login_required
@check_usage_limit('qr')
def generate_qr():
    """生成QR码"""
    try:
        data = request.get_json()
        
        qr_data = data.get('data', '')
        qr_type = data.get('type', 'text')
        
        if not qr_data:
            return jsonify({'error': '请提供要编码的数据'}), 400
        
        # 生成QR码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
            # 保存文件
            filename = f"qr_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        img.save(filepath)
        
        # 记录使用次数
        current_user.qr_usage_count += 1
        db.session.commit()
        
        # 保存记录
        record = QRRecord(
            user_id=current_user.id,
            qr_type=qr_type,
            content_data=qr_data,
            file_path=filepath
        )
        db.session.add(record)
        db.session.commit()
        
        # 返回base64图片
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'data': img_base64,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users')
@login_required
@admin_required
def admin_users():
    """管理员获取用户列表"""
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'plan_type': user.plan_type,
        'dm_usage_count': user.dm_usage_count,
        'qr_usage_count': user.qr_usage_count,
        'created_at': user.created_at.isoformat(),
        'is_active': user.is_active
    } for user in users])

@app.route('/api/admin/stats')
@login_required
@admin_required
def admin_stats():
    """管理员获取统计信息"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_dm = db.session.query(db.func.sum(User.dm_usage_count)).scalar() or 0
    total_qr = db.session.query(db.func.sum(User.qr_usage_count)).scalar() or 0
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'total_dm_generated': total_dm,
        'total_qr_generated': total_qr
    })

# 初始化数据库
@app.before_first_request
def create_tables():
    db.create_all()
    
    # 创建默认管理员账户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            plan_type='enterprise',
            dm_monthly_limit=999999,
            qr_monthly_limit=999999
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    print("🚀 整合平台启动中...")
    print("=" * 50)
    print("访问地址: http://localhost:5000")
    print("默认管理员: admin / admin123")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
