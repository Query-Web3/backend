# QueryWeb3 Backend

QueryWeb3是一个区块链数据查询系统的后端服务，提供链上交易数据统计和收益率查询功能。

## 1. 项目环境要求

- Python 3.10+
- MySQL 8.0+
- pip 包管理器

### 系统依赖
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PyMySQL 1.1.0
- Pydantic 2.5.2
- uvicorn 0.24.0
- python-dotenv 1.0.0

## 2. 项目结构

```
queryweb3-backend/
├── app/                        # 应用主目录
│   ├── api/                   # API路由目录
│   │   └── v1/               # API版本1
│   │       └── endpoints.py   # API端点定义
│   ├── core/                 # 核心配置目录
│   │   └── config.py         # 配置文件
│   ├── db/                   # 数据库相关
│   │   └── session.py        # 数据库会话管理
│   ├── models/               # 数据模型
│   │   ├── base.py          # 基础模型
│   │   └── models.py        # SQLAlchemy模型定义
│   ├── schemas/             # Pydantic模型
│   │   └── schemas.py       # 请求响应模型
│   └── main.py             # 应用入口文件
├── database/               # 数据库脚本
│   └── init.sql           # 数据库初始化脚本
├── requirements.txt       # 项目依赖
├── .env.example          # 环境变量示例
└── README.md             # 项目说明文档
```

## 3. 如何运行

### 3.1 环境准备

1. 克隆项目：
```bash
git clone <repository_url>
cd queryweb3-backend
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 3.2 数据库配置

1. 复制环境变量配置：
```bash
cp .env.example .env
```

2. 修改 `.env` 文件，填入你的数据库配置：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASS=your_password
DB_NAME=queryweb3
```

3. 初始化数据库：
```bash
mysql -u your_username -p < database/init.sql
```

### 3.3 启动服务

1. 开发模式启动：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. 生产模式启动：
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 4. API文档

启动服务后，可以通过以下地址访问API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 5. API示例

### 5.1 交易量查询

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/vol-txns/' \
  -H 'Content-Type: application/json' \
  -d '{
  "from_date": "2025-01-01",
  "to_date": "2025-01-19",
  "chain": "Ethereum",
  "cycle": "daily"
}'
```

### 5.2 收益率查询

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/yield/' \
  -H 'Content-Type: application/json' \
  -d '{
  "date": "2025-01-19",
  "chain": "Ethereum",
  "asset_type": "DeFi",
  "return_type": "Staking",
  "token": "ETH"
}'
```

## 6. 数据库表结构

主要表结构说明：

- `chains`: 区块链网络信息
- `asset_types`: 资产类型（DeFi、GameFi等）
- `return_types`: 收益类型（Staking、Farming等）
- `tokens`: 代币信息
- `token_daily_stats`: 代币每日统计数据
- `yield_stats`: 收益率数据
- `stat_cycles`: 统计周期定义

详细的表结构请参考 `database/init.sql`。

## 7. 开发指南

### 7.1 添加新的API端点

1. 在 `app/schemas/schemas.py` 中定义请求和响应模型
2. 在 `app/api/v1/endpoints.py` 中添加新的路由处理函数
3. 如需要，在 `app/models/models.py` 中添加新的数据模型

### 7.2 数据库迁移

当前版本使用原生SQL进行数据库管理。如需要进行数据库迁移，建议：

1. 在 `database/migrations/` 目录下创建迁移脚本
2. 按照时间戳命名迁移文件
3. 记录所有数据库变更

## 8. 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 9. 许可证

[MIT License](LICENSE)
