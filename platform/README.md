# 整合平台 - DM自动生产器 & QR永久生产器

这是一个整合了DM自动生产器和QR永久生产器的完整平台，提供用户管理、账户系统、使用统计和后台管理功能。

## 功能特色

### 🎨 DM自动生产器
- 多种预设模板
- 自定义样式和颜色主题
- 商品管理和批量生成
- 高质量导出功能
- 使用次数限制和统计

### 📱 QR永久生产器
- 支持多种QR码类型（文本、URL、WiFi、邮件、电话、短信、联系人）
- 批量生成功能
- 永久保存和下载
- 生成历史记录
- 使用次数限制和统计

### 👥 用户管理系统
- 用户注册和登录
- 个人资料管理
- 使用统计和进度显示
- 方案管理和升级

### 🛡️ 权限管理
- 用户认证和会话管理
- 使用限制检查
- 管理员权限控制
- 数据安全保护

### 📊 后台管理
- 用户管理
- 使用统计
- 方案管理
- 系统设置

## 技术栈

- **后端**: Flask + SQLAlchemy + Flask-Login
- **前端**: HTML5 + Tailwind CSS + Alpine.js
- **数据库**: SQLite
- **QR码生成**: qrcode (Python)
- **图像处理**: Pillow

## 安装和运行

### 1. 环境要求
- Python 3.7+
- pip

### 2. 克隆项目
```bash
git clone https://github.com/yourusername/platform.git
cd platform
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
# 复制环境变量示例文件
cp env.example .env

# 编辑 .env 文件，设置你的配置
```

### 5. 启动应用
```bash
# 开发环境
python app.py

# 或使用启动脚本 (Windows)
start.bat
```

### 6. 访问应用
- 访问地址: http://localhost:5000
- 默认管理员账户: admin / admin123

## 部署到生产环境

### Heroku 部署
1. 创建 Heroku 应用
2. 设置环境变量
3. 推送代码到 Heroku

### 传统服务器部署
1. 安装 Python 和依赖
2. 配置 Nginx 反向代理
3. 使用 Gunicorn 运行应用
4. 设置环境变量

## 使用说明

### 用户注册和登录
1. 访问首页，点击"立即开始"或"注册"
2. 填写用户名、邮箱和密码
3. 注册成功后自动登录

### DM生成器使用
1. 登录后进入"DM生成器"页面
2. 选择模板和配置样式
3. 添加商品信息
4. 选择DM方案
5. 点击"生成DM"创建内容
6. 下载或分享生成的DM

### QR生成器使用
1. 进入"QR生成器"页面
2. 选择QR码类型
3. 填写相应的内容信息
4. 点击"生成QR码"
5. 下载或分享生成的QR码

### 个人资料管理
1. 进入"个人资料"页面
2. 查看使用统计和方案信息
3. 修改个人信息
4. 升级方案（如需要）

### 管理员功能
1. 使用管理员账户登录
2. 进入"管理后台"
3. 查看系统统计
4. 管理用户账户
5. 配置系统设置

## 方案说明

### 免费方案
- DM生成：10次/月
- QR生成：50次/月
- 基础模板
- 社区支持

### 基础方案 (¥29/月)
- DM生成：100次/月
- QR生成：500次/月
- 高级模板
- 优先支持

### 企业方案 (¥99/月)
- DM生成：无限制
- QR生成：无限制
- 所有模板
- 专属支持

## 文件结构

```
platform/
├── app.py                 # 主应用文件
├── requirements.txt       # Python依赖
├── start.bat             # Windows启动脚本
├── templates/            # HTML模板
│   ├── base.html         # 基础模板
│   ├── index.html        # 首页
│   ├── login.html        # 登录页
│   ├── register.html     # 注册页
│   ├── dashboard.html    # 仪表板
│   ├── dm_generator.html # DM生成器
│   ├── qr_generator.html # QR生成器
│   ├── profile.html      # 个人资料
│   └── admin.html        # 管理后台
├── static/               # 静态文件
│   └── js/               # JavaScript文件
│       ├── dm-generator.js
│       └── qr-generator.js
├── uploads/              # 上传文件目录
├── generated_files/      # 生成文件目录
└── platform.db          # SQLite数据库
```

## API接口

### 用户相关
- `POST /login` - 用户登录
- `POST /register` - 用户注册
- `GET /logout` - 用户退出
- `GET /api/user/stats` - 获取用户统计

### DM生成
- `POST /api/dm/generate` - 生成DM

### QR生成
- `POST /api/qr/generate` - 生成QR码

### 管理员
- `GET /api/admin/users` - 获取用户列表
- `GET /api/admin/stats` - 获取系统统计

## 数据库模型

### User (用户)
- id, username, email, password_hash
- plan_type, dm_usage_count, qr_usage_count
- dm_monthly_limit, qr_monthly_limit
- is_admin, is_active, created_at

### DMRecord (DM记录)
- id, user_id, template_name, content_data
- created_at, file_path

### QRRecord (QR记录)
- id, user_id, qr_type, content_data
- created_at, file_path

### Payment (支付记录)
- id, user_id, plan_type, amount
- status, created_at, expires_at

## 安全特性

- 密码哈希存储
- 用户会话管理
- 使用限制检查
- 权限验证
- 数据验证和清理

## 部署建议

### 开发环境
- 使用SQLite数据库
- 启用调试模式
- 使用内置服务器

### 生产环境
- 使用PostgreSQL或MySQL
- 配置反向代理（Nginx）
- 使用WSGI服务器（Gunicorn）
- 配置HTTPS
- 设置环境变量

## 常见问题

### Q: 如何重置管理员密码？
A: 删除数据库文件，重新启动应用会自动创建默认管理员账户。

### Q: 如何修改使用限制？
A: 在数据库中直接修改用户的monthly_limit字段，或通过管理后台修改。

### Q: 如何备份数据？
A: 复制platform.db文件即可备份所有数据。

### Q: 如何添加新的QR码类型？
A: 修改qr_generator.js中的getQRData()方法和相关验证逻辑。

## 更新日志

### v1.0.0 (2024-01-15)
- 初始版本发布
- 整合DM和QR生成器
- 用户管理系统
- 后台管理功能
- 使用统计和限制

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请联系：
- 邮箱: support@example.com
- 项目地址: https://github.com/example/platform
