# QueryWeb3 后端服务

QueryWeb3 后端服务是一个基于 FastAPI 的区块链数据查询服务，提供高性能的 API 接口，支持多链数据查询、数据分析和可视化功能。

## 项目环境

### 系统要求
- Python 3.10+
- MySQL 8.0+

### 依赖包
主要依赖包版本要求：
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
python-dotenv==1.0.0
pydantic==2.5.2
pydantic-settings==2.1.0
python-jose==3.3.0
python-multipart==0.0.6
cryptography==41.0.5
```

测试相关依赖：
```
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
pytest-cov==4.1.0
```

完整依赖列表请参见 `requirements.txt`。

## 项目结构

```
queryweb3-backend/
├── app/                 # 应用主目录
│   ├── api/            # API 相关代码
│   │   └── v1/         # API v1 版本
│   │       └── endpoints.py  # API 端点定义
│   ├── core/           # 核心配置
│   │   └── config.py   # 配置管理
│   ├── db/             # 数据库相关
│   ├── models/         # 数据模型
│   ├── schemas/        # Pydantic 模型
│   └── main.py         # 应用入口
├── database/           # 数据库相关文件
├── tests/              # 测试目录
│   ├── api/            # API 测试
│   │   └── v1/         # v1 API 测试
│   ├── utils/          # 测试工具
│   │   ├── check_vol_txns.py    # 交易量数据检查
│   │   └── check_yield_dates.py # 收益率数据检查
│   ├── conftest.py     # 测试配置
│   └── test_api.py     # API 测试用例
├── .env                # 环境变量配置
├── .env.example        # 环境变量示例
├── requirements.txt    # 项目依赖
└── README.md           # 项目文档
```

## 环境配置

1. 克隆项目：
```bash
git clone <repository-url>
cd queryweb3-backend
```

2. 创建虚拟环境：
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

4. 配置环境变量：
```bash
cp .env.example .env
```
编辑 `.env` 文件，设置必要的环境变量：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASS=your_password
DB_NAME=queryweb3
```

## 数据库设置

1. 创建数据库：
```bash
mysql -u root -p
CREATE DATABASE queryweb3;
```

2. 运行数据库迁移：
```bash
alembic upgrade head
```

## 启动服务

### 开发环境
```bash
uvicorn app.main:app --reload --port 8000
```

### 生产环境
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

服务将在 http://localhost:8000 运行，API 文档可在 http://localhost:8000/docs 查看。

## API 文档

### 主要端点

1. 交易量查询
```
POST /api/v1/vol-txns
请求体：
{
    "from_date": "2024-10-18",
    "to_date": "2025-01-26",
    "chain": "Hydration",
    "cycle": "daily"
}
```

2. 收益率查询
```
GET /api/v1/yield
参数：
- date: 日期
- chain: 链名称
- asset_type: 资产类型
- return_type: 收益类型
```

详细的 API 文档请访问运行中的服务的 `/docs` 或 `/redoc` 端点。

## 测试

### 测试环境设置

1. 配置测试环境变量：
```env
TEST_API_URL=http://localhost:8000
```

### 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_api.py

# 带覆盖率报告的测试
pytest --cov=app tests/
```

### 测试工具

项目包含以下测试工具脚本：

- `tests/utils/check_vol_txns.py`: 用于检查交易量数据和统计
- `tests/utils/check_yield_dates.py`: 用于检查收益率数据和日期范围

运行测试工具：
```bash
python -m tests.utils.check_vol_txns
python -m tests.utils.check_yield_dates
```

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

MIT

本项目采用 MIT 许可证 - 详见 LICENSE 文件