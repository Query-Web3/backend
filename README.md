# QueryWeb3 后端服务

QueryWeb3 后端服务是一个基于 FastAPI 的区块链数据查询服务，提供高性能的 API 接口，支持多链数据查询、数据分析和可视化功能。

## 项目环境

### 系统要求
- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Docker (可选)

### 依赖包
主要依赖包版本要求：
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.2
aiohttp==3.9.1
web3==6.11.3
redis==5.0.1
```

完整依赖列表请参见 `requirements.txt`。

## 项目结构

```
queryweb3-backend/
├── app/                    # 应用主目录
│   ├── api/               # API 相关代码
│   │   ├── v1/           # API v1 版本
│   │   │   ├── endpoints/    # API 端点定义
│   │   │   │   ├── vol_txns.py   # 交易量相关接口
│   │   │   │   └── yield.py      # 收益率相关接口
│   │   │   └── api.py      # API 路由配置
│   │   └── deps.py     # 依赖注入
│   ├── core/           # 核心配置
│   │   ├── config.py   # 配置管理
│   │   └── security.py # 安全相关
│   ├── db/             # 数据库相关
│   │   ├── base.py     # 数据库基类
│   │   └── session.py  # 数据库会话
│   ├── models/         # 数据模型
│   │   ├── base.py     # 基础模型
│   │   └── blockchain.py # 区块链数据模型
│   ├── schemas/        # Pydantic 模型
│   │   └── blockchain.py # 数据验证模型
│   ├── services/       # 业务逻辑
│   │   ├── blockchain.py # 区块链数据服务
│   │   └── cache.py    # 缓存服务
│   └── main.py         # 应用入口
├── tests/              # 测试目录
│   ├── conftest.py     # 测试配置
│   └── api/            # API 测试
├── alembic/            # 数据库迁移
│   ├── versions/       # 迁移文件
│   └── env.py         # 迁移环境
├── scripts/           # 实用脚本
│   └── init_db.py    # 数据库初始化
├── docker/           # Docker 相关文件
│   ├── Dockerfile    # 应用 Dockerfile
│   └── docker-compose.yml # 容器编排
├── .env.example      # 环境变量示例
├── alembic.ini       # Alembic 配置
├── requirements.txt  # 项目依赖
└── README.md         # 项目文档
```

## 环境配置

1. 克隆项目：
```bash
git clone https://github.com/Query-Web3/backend.git
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
DATABASE_URL=postgresql://user:password@localhost:5432/queryweb3
REDIS_URL=redis://localhost:6379/0
API_KEY=your_api_key
BLOCKCHAIN_RPC_URLS={"ethereum":"https://eth-mainnet.alchemyapi.io/v2/your-key"}
```

## 数据库设置

1. 创建数据库：
```bash
createdb queryweb3
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

### Docker 部署
```bash
docker-compose up -d
```

服务将在 http://localhost:8000 运行，API 文档可在 http://localhost:8000/docs 查看。

## API 文档

### 主要端点

1. 交易量查询
```
GET /api/v1/vol-txns/
参数：
- date: 日期
- chain: 链名称
- token: 代币名称
```

2. 收益率查询
```
GET /api/v1/yield/
参数：
- date: 日期
- chain: 链名称
- asset_type: 资产类型
- return_type: 收益类型
```

详细的 API 文档请访问运行中的服务的 `/docs` 或 `/redoc` 端点。

## 测试

运行测试：
```bash
pytest
```

运行覆盖率报告：
```bash
pytest --cov=app tests/
```

## 监控和日志

- 日志文件位于 `logs/` 目录
- 使用 Prometheus 进行指标收集
- Grafana 仪表板模板位于 `monitoring/` 目录

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 联系方式

- 项目维护者：oss-jtyd
- 邮箱：oss.jtyd@gmail.com
- 项目链接：[https://github.com/Query-Web3/backend](https://github.com/Query-Web3/backend)