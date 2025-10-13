import os
from datetime import timedelta

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///platform.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'generated_files'
    
    # 用户配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 使用限制配置
    FREE_PLAN_DM_LIMIT = 10
    FREE_PLAN_QR_LIMIT = 50
    BASIC_PLAN_DM_LIMIT = 100
    BASIC_PLAN_QR_LIMIT = 500
    ENTERPRISE_PLAN_DM_LIMIT = 999999
    ENTERPRISE_PLAN_QR_LIMIT = 999999

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///platform_dev.db'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///platform.db'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
