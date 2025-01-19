# QueryWeb3 后端服务

QueryWeb3 后端服务是一个基于 FastAPI 的区块链数据查询服务，提供高性能的 API 接口，支持多链数据查询、数据分析和可视化功能。

## 项目环境

### 系统要求
- Python 3.10
- MySQL 8.0+
- Redis 6+
- Docker (可选)

### 依赖包
主要依赖包版本要求：
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
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
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/queryweb3
REDIS_URL=redis://localhost:6379/0
API_KEY=your_api_key
BLOCKCHAIN_RPC_URLS={"ethereum":"https://eth-mainnet.alchemyapi.io/v2/your-key"}
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
- page: 页码（默认1）
- page_size: 每页记录数（默认10，最大100）
```

详细的 API 文档请访问运行中的服务的 `/docs` 或 `/redoc` 端点。

## 测试

### 测试环境设置

1. 安装测试依赖：
```bash
pip install -r tests/requirements.txt
```

2. 配置测试环境：
创建 `.env` 文件在 tests 目录下：
```env
TEST_API_URL=http://localhost:8000
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/api/v1/test_endpoints.py

# 运行特定测试类
pytest tests/api/v1/test_endpoints.py::TestYieldEndpoint

# 运行特定测试方法
pytest tests/api/v1/test_endpoints.py::TestYieldEndpoint::test_yield_query_success
```

### 测试覆盖范围

1. Yield 接口测试：
- 基本查询功能
- 分页功能
- 无效的链名称
- 返回数据结构验证

2. VolTxns 接口测试：
- 基本查询功能
- 无效的链名称
- 无效的日期范围
- 返回数据结构验证

### 添加新测试

在 `tests/api/v1/test_endpoints.py` 中添加新的测试用例：

```python
def test_new_feature(self):
    """测试新功能"""
    payload = {
        "param1": "value1",
        "param2": "value2"
    }
    response = requests.post(self.ENDPOINT_URL, json=payload)
    assert response.status_code == 200
    # 添加更多断言...
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