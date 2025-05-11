from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.schemas import (
    VolTxnsQuery, YieldQuery,
    VolTxnsListResponse, YieldListResponse
)
from sqlalchemy import select, and_
from app.models.models import (
    Chain, Token, TokenDailyStat, YieldStat, StatCycle, AssetType, ReturnType
)
from datetime import timedelta

router = APIRouter()


@router.post("/vol-txns", response_model=VolTxnsListResponse)
async def get_vol_txns(
    query: VolTxnsQuery,
    db: Session = Depends(get_db)
):
    # 验证日期范围
    if query.from_date > query.to_date:
        raise HTTPException(
            status_code=400,
            detail="Invalid date range: from_date must be earlier than or equal to to_date"
        )

    # 获取统计周期
    cycle = db.query(StatCycle).filter(StatCycle.name == query.cycle).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Invalid cycle")

    # 构建基础查询
    base_query = db.query(
        TokenDailyStat,
        Token.symbol,
        Chain.name.label('chain')
    ).join(
        Token, Token.id == TokenDailyStat.token_id
    ).join(
        Chain, Chain.id == Token.chain_id
    )

    # 构建过滤条件
    filters = [TokenDailyStat.date.between(query.from_date, query.to_date)]

    # 如果指定了链，添加链的过滤条件
    if query.chain:
        chain = db.query(Chain).filter(Chain.name == query.chain).first()
        if not chain:
            raise HTTPException(status_code=404, detail="Chain not found")
        filters.append(Token.chain_id == chain.id)

    # 执行查询，按交易量从高到低排序
    results = base_query.filter(and_(*filters)).order_by(TokenDailyStat.volume.desc()).all()
    print(f"DEBUG: Query results count: {len(results)}")
    print(f"DEBUG: Query filters: {filters}")
    print(f"DEBUG: First result: {results[0] if results else None}")

    response_data = []
    for stat, token_symbol, chain in results:
        print(f"DEBUG: Processing row - stat={stat.date}, token={token_symbol}, chain={chain}")
        response_data.append({
            "time": stat.date,
            "volume": stat.volume,
            "yoy": stat.volume_yoy,
            "qoq": stat.volume_qoq,
            "txns": stat.txns_count,
            "txns_yoy": stat.txns_yoy,
            "txns_qoq": stat.txns_qoq,
            "token": token_symbol,
            "chain": chain
        })

    response = {
        "data": response_data,
        "total": len(response_data)
    }
    print(f"DEBUG: Final response data count: {len(response_data)}")
    print(f"DEBUG: First response item: {response_data[0] if response_data else None}")
    return response


@router.post("/yield", response_model=YieldListResponse)
async def get_yield(
    query: YieldQuery,
    db: Session = Depends(get_db)
):
    # 构建基础查询
    base_query = db.query(
        YieldStat,
        Token.symbol,
        TokenDailyStat.price_usd,
        Chain.name.label('chain_name'),
        ReturnType.name.label('return_type_name'),
        AssetType.name.label('asset_type_name')
    ).join(
        Token, Token.id == YieldStat.token_id
    ).join(
        TokenDailyStat, (TokenDailyStat.token_id == Token.id) & (TokenDailyStat.date == query.date)
    ).join(
        ReturnType, ReturnType.id == YieldStat.return_type_id
    ).join(
        Chain, Chain.id == Token.chain_id
    ).join(
        AssetType, AssetType.id == Token.asset_type_id
    )

    # 构建过滤条件
    filters = [YieldStat.date == query.date]

    # 如果指定了链，添加链的过滤条件
    if query.chain:
        chain = db.query(Chain).filter(Chain.name == query.chain).first()
        if chain:
            filters.append(Chain.id == chain.id)

    # 如果指定了资产类型，添加资产类型的过滤条件
    if query.asset_type:
        asset_type = db.query(AssetType).filter(AssetType.name == query.asset_type).first()
        if asset_type:
            filters.append(Token.asset_type_id == asset_type.id)

    # 添加可选过滤条件
    if query.return_type:
        return_type = db.query(ReturnType).filter(ReturnType.name == query.return_type).first()
        if return_type:
            filters.append(YieldStat.return_type_id == return_type.id)

    if query.token:
        filters.append(Token.symbol == query.token)

    # 计算总记录数
    total_records = base_query.filter(and_(*filters)).count()
    
    # 计算分页信息
    total_pages = (total_records + query.page_size - 1) // query.page_size
    offset = (query.page - 1) * query.page_size

    # 执行分页查询，按 APY 从高到低排序
    results = base_query.filter(and_(*filters)).order_by(YieldStat.apy.desc()).offset(offset).limit(query.page_size).all()

    # 获取24小时数据
    yesterday = query.date - timedelta(days=1)
    yesterday_stats = {
        (stat.token_id, stat.return_type_id): stat
        for stat in db.query(YieldStat).filter(and_(
            YieldStat.date == yesterday,
            YieldStat.token_id.in_([r.YieldStat.token_id for r in results])
        )).all()
    }
    
    response_data = []
    for item in results:
        # 获取昨日数据
        yesterday_stat = db.query(
            YieldStat,
            TokenDailyStat.volume_usd
        ).join(
            Token, Token.id == YieldStat.token_id
        ).join(
            TokenDailyStat, (TokenDailyStat.token_id == Token.id) & (TokenDailyStat.date == yesterday)
        ).filter(
            YieldStat.token_id == item.YieldStat.token_id,
            YieldStat.date == yesterday
        ).first()

        # 构建响应数据
        yield_data = {
            "token": item.symbol,
            "apy": float(item.YieldStat.apy),
            "tvl_usd": float(item.YieldStat.tvl_usd),
            "price_usd": float(item.price_usd) if item.price_usd else 0,
            "chain": item.chain_name,
            "return_type": item.return_type_name,
            "vol_24h_usd": float(yesterday_stat.volume_usd) if yesterday_stat else 0,
            "txns_24h": 0,
            "asset_type": item.asset_type_name,
            "date": item.YieldStat.date
        }

        response_data.append(yield_data)

    return {
        "data": response_data,
        "total": total_records,
        "page": query.page,
        "page_size": query.page_size,
        "total_pages": total_pages,
        "has_next": query.page < total_pages,
        "has_prev": query.page > 1
    }


@router.get("/chains", response_model=List[str])
async def get_chains(db: Session = Depends(get_db)):
    """获取所有可用的区块链网络列表"""
    chains = db.query(Chain.name).all()
    return [chain[0] for chain in chains]


@router.get("/cycles", response_model=List[str])
async def get_cycles(db: Session = Depends(get_db)):
    """获取所有可用的区块链网络列表"""
    chains = db.query(StatCycle.name).all()
    return [chain[0] for chain in chains]


@router.get("/asset-types", response_model=List[str])
async def get_asset_types(db: Session = Depends(get_db)):
    """获取所有可用的资产类型列表"""
    asset_types = db.query(AssetType.name).all()
    return [asset_type[0] for asset_type in asset_types]


@router.get("/return-types", response_model=List[str])
async def get_return_types(db: Session = Depends(get_db)):
    """获取所有可用的收益类型列表"""
    return_types = db.query(ReturnType.name).all()
    return [return_type[0] for return_type in return_types]


@router.get("/tokens", response_model=List[str])
async def get_tokens(
    chain: Optional[str] = None,
    asset_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取代币列表，可以按链和资产类型筛选"""
    query = db.query(Token.symbol).select_from(Token)
    
    if chain:
        query = query.join(Chain, Token.chain_id == Chain.id).filter(Chain.name == chain)
    
    if asset_type:
        query = query.join(AssetType, Token.asset_type_id == AssetType.id).filter(AssetType.name == asset_type)
    
    tokens = query.all()
    return [token[0] for token in tokens]
