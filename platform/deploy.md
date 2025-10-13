# 部署指南

## GitHub 部署准备

### 1. 创建 GitHub 仓库
```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: 整合平台 v1.0.0"

# 添加远程仓库
git remote add origin https://github.com/yourusername/platform.git

# 推送到 GitHub
git push -u origin main
```

### 2. 设置 GitHub Pages (可选)
如果要在 GitHub Pages 上部署静态版本，需要：
- 创建 `docs/` 文件夹
- 将静态文件放入其中
- 在仓库设置中启用 GitHub Pages

## Heroku 部署

### 1. 安装 Heroku CLI
```bash
# 下载并安装 Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli
```

### 2. 创建 Heroku 应用
```bash
# 登录 Heroku
heroku login

# 创建应用
heroku create your-app-name

# 设置环境变量
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-production-secret-key
```

### 3. 部署到 Heroku
```bash
# 推送代码
git push heroku main

# 运行数据库迁移
heroku run python -c "from app import db; db.create_all()"
```

## 传统服务器部署

### 1. 服务器准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和 pip
sudo apt install python3 python3-pip python3-venv -y

# 安装 Nginx
sudo apt install nginx -y
```

### 2. 应用部署
```bash
# 克隆代码
git clone https://github.com/yourusername/platform.git
cd platform

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
```

### 3. 配置 Gunicorn
```bash
# 安装 Gunicorn
pip install gunicorn

# 创建 Gunicorn 配置文件
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
EOF

# 启动应用
gunicorn -c gunicorn.conf.py app:app
```

### 4. 配置 Nginx
```bash
# 创建 Nginx 配置
sudo cat > /etc/nginx/sites-available/platform << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /path/to/platform/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用站点
sudo ln -s /etc/nginx/sites-available/platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 设置系统服务
```bash
# 创建 systemd 服务文件
sudo cat > /etc/systemd/system/platform.service << EOF
[Unit]
Description=Platform Gunicorn Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/platform
Environment="PATH=/path/to/platform/venv/bin"
ExecStart=/path/to/platform/venv/bin/gunicorn -c gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start platform
sudo systemctl enable platform
```

## 环境变量配置

### 开发环境
```bash
FLASK_ENV=development
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///platform_dev.db
```

### 生产环境
```bash
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=postgresql://user:password@localhost/platform
```

## 数据库配置

### SQLite (开发环境)
- 默认配置，无需额外设置
- 数据库文件会自动创建

### PostgreSQL (生产环境)
```bash
# 安装 PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# 创建数据库和用户
sudo -u postgres psql
CREATE DATABASE platform;
CREATE USER platform_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE platform TO platform_user;
\q

# 更新 DATABASE_URL
export DATABASE_URL=postgresql://platform_user:your_password@localhost/platform
```

## SSL 证书配置

### 使用 Let's Encrypt
```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

## 监控和日志

### 日志配置
```bash
# 创建日志目录
sudo mkdir -p /var/log/platform
sudo chown www-data:www-data /var/log/platform

# 配置日志轮转
sudo cat > /etc/logrotate.d/platform << EOF
/var/log/platform/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload platform
    endscript
}
EOF
```

### 监控脚本
```bash
# 创建健康检查脚本
cat > health_check.sh << EOF
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ $response -eq 200 ]; then
    echo "Service is healthy"
    exit 0
else
    echo "Service is unhealthy"
    exit 1
fi
EOF

chmod +x health_check.sh
```

## 备份策略

### 数据库备份
```bash
# 创建备份脚本
cat > backup.sh << EOF
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/platform"
mkdir -p $BACKUP_DIR

# 备份数据库
pg_dump $DATABASE_URL > $BACKUP_DIR/platform_$DATE.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz uploads/

# 清理旧备份 (保留30天)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x backup.sh

# 设置定时备份
crontab -e
# 添加以下行 (每天凌晨2点备份)
0 2 * * * /path/to/backup.sh
```
