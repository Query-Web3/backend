import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_chains():
    """测试获取链列表接口"""
    response = client.get("/api/v1/chains")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # 检查是否包含初始化的链
    chains = response.json()
    expected_chains = ["Polkadot", "Kusama", "Hydration", "Bifrost"]
    assert all(chain in chains for chain in expected_chains)


def test_get_asset_types():
    """测试获取资产类型列表接口"""
    response = client.get("/api/v1/asset-types")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # 检查是否包含初始化的资产类型
    asset_types = response.json()
    expected_types = ["DeFi", "GameFi", "NFT"]
    assert all(type_ in asset_types for type_ in expected_types)


def test_get_return_types():
    """测试获取收益类型列表接口"""
    response = client.get("/api/v1/return-types")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # 检查是否包含初始化的收益类型
    return_types = response.json()
    expected_types = ["Staking", "Farming", "Lending"]
    assert all(type_ in return_types for type_ in expected_types)


def test_get_tokens():
    """测试获取代币列表接口"""
    # 测试无参数获取所有代币
    response = client.get("/api/v1/tokens")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # 测试按链筛选
    response = client.get("/api/v1/tokens?chain=Hydration")
    assert response.status_code == 200
    tokens = response.json()
    assert isinstance(tokens, list)

    # 测试按资产类型筛选
    response = client.get("/api/v1/tokens?asset_type=DeFi")
    assert response.status_code == 200
    tokens = response.json()
    assert isinstance(tokens, list)

    # 测试组合筛选
    response = client.get("/api/v1/tokens?chain=Hydration&asset_type=DeFi")
    assert response.status_code == 200
    tokens = response.json()
    assert isinstance(tokens, list)


def test_yield_api():
    """测试收益率查询接口"""
    payload = {
        "asset_type": "DeFi",
        "chain": "Hydration",
        "date": "2022-01-01",
        "page": 1,
        "page_size": 10,
        "return_type": "Staking"
    }
    response = client.post("/api/v1/yield", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
