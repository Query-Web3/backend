import pytest
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取测试环境的API URL
API_URL = os.getenv("TEST_API_URL", "http://localhost:8000")

class TestYieldEndpoint:
    YIELD_URL = f"{API_URL}/api/v1/yield/"

    def test_yield_query_success(self):
        """测试收益率查询接口 - 成功场景"""
        payload = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "chain": "Hydration",
            "asset_type": "DeFi",
            "return_type": "Staking",
            "page": 1,
            "page_size": 10
        }
        
        response = requests.post(self.YIELD_URL, json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert "total_pages" in data
        assert "has_next" in data
        assert "has_prev" in data
        
        # 验证分页
        assert data["page"] == payload["page"]
        assert data["page_size"] == payload["page_size"]
        assert isinstance(data["total"], int)
        
        # 验证数据结构
        if data["data"]:
            first_item = data["data"][0]
            assert "token" in first_item
            assert "apy" in first_item
            assert "tvl_usd" in first_item
            assert "price_usd" in first_item
            assert "chain" in first_item
            assert "return_type" in first_item
            assert "vol_24h_usd" in first_item
            assert "txns_24h" in first_item
            assert "asset_type" in first_item
            assert "date" in first_item

    def test_yield_query_invalid_chain(self):
        """测试收益率查询接口 - 无效的链"""
        payload = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "chain": "invalid_chain",
            "asset_type": "DeFi",
            "page": 1,
            "page_size": 10
        }
        
        response = requests.post(self.YIELD_URL, json=payload)
        assert response.status_code == 404
        assert "Chain not found" in response.json()["detail"]

    def test_yield_query_pagination(self):
        """测试收益率查询接口 - 分页功能"""
        # 测试第一页
        payload = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "chain": "Hydration",
            "asset_type": "DeFi",
            "page": 1,
            "page_size": 5
        }
        
        response = requests.post(self.YIELD_URL, json=payload)
        assert response.status_code == 200
        first_page = response.json()
        
        # 测试第二页
        payload["page"] = 2
        response = requests.post(self.YIELD_URL, json=payload)
        assert response.status_code == 200
        second_page = response.json()
        
        # 验证分页
        if first_page["total"] > payload["page_size"]:
            assert first_page["has_next"] is True
            assert len(first_page["data"]) == payload["page_size"]
            # 确保第一页和第二页数据不重复
            first_page_tokens = {item["token"] for item in first_page["data"]}
            second_page_tokens = {item["token"] for item in second_page["data"]}
            assert not first_page_tokens.intersection(second_page_tokens)


class TestVolTxnsEndpoint:
    VOL_TXNS_URL = f"{API_URL}/api/v1/vol-txns/"

    def test_vol_txns_query_success(self):
        """测试交易量查询接口 - 成功场景"""
        payload = {
            "from_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "to_date": datetime.now().strftime("%Y-%m-%d"),
            "chain": "Hydration",
            "cycle": "daily"
        }
        
        response = requests.post(self.VOL_TXNS_URL, json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "total" in data
        
        # 验证数据结构
        if data["data"]:
            first_item = data["data"][0]
            assert "time" in first_item
            assert "volume" in first_item
            assert "yoy" in first_item
            assert "qoq" in first_item
            assert "txns" in first_item
            assert "txns_yoy" in first_item

    def test_vol_txns_query_invalid_chain(self):
        """测试交易量查询接口 - 无效的链"""
        payload = {
            "from_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "to_date": datetime.now().strftime("%Y-%m-%d"),
            "chain": "invalid_chain",
            "cycle": "daily"
        }
        
        response = requests.post(self.VOL_TXNS_URL, json=payload)
        assert response.status_code == 404
        assert "Chain not found" in response.json()["detail"]

    def test_vol_txns_query_invalid_date_range(self):
        """测试交易量查询接口 - 无效的日期范围"""
        payload = {
            "from_date": datetime.now().strftime("%Y-%m-%d"),
            "to_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),  # 结束日期早于开始日期
            "chain": "Hydration",
            "cycle": "daily"
        }
        
        response = requests.post(self.VOL_TXNS_URL, json=payload)
        assert response.status_code == 400  # 应该返回400 Bad Request
