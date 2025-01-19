from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import (
    VolTxnsQuery, YieldQuery,
    VolTxnsListResponse, YieldListResponse
)
from sqlalchemy import select, and_
from app.models.models import (
    Chain, Token, TokenDailyStat, YieldStat,
    AssetType, ReturnType, StatCycle
)
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/vol-txns/", response_model=VolTxnsListResponse)
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

    # 获取chain_id
    chain = db.query(Chain).filter(Chain.name == query.chain).first()
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")

    # 获取统计周期
    cycle = db.query(StatCycle).filter(StatCycle.name == query.cycle).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Invalid cycle")

    # 构建查询
    stmt = select(TokenDailyStat).join(Token).join(Chain).where(
        and_(
            Chain.id == chain.id,
            TokenDailyStat.date.between(query.from_date, query.to_date)
        )
    ).order_by(TokenDailyStat.date)

    results = db.execute(stmt).scalars().all()
    
    response_data = []
    for stat in results:
        response_data.append({
            "time": stat.date,
            "volume": stat.volume,
            "yoy": stat.volume_yoy,
            "qoq": stat.volume_qoq,
            "txns": stat.txns_count,
            "txns_yoy": stat.txns_yoy
        })

    return {
        "data": response_data,
        "total": len(response_data)
    }

@router.post("/yield/", response_model=YieldListResponse)
async def get_yield(
    query: YieldQuery,
    db: Session = Depends(get_db)
):
    # 获取chain
    chain = db.query(Chain).filter(Chain.name == query.chain).first()
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")

    # 获取asset_type
    asset_type = db.query(AssetType).filter(AssetType.name == query.asset_type).first()
    if not asset_type:
        raise HTTPException(status_code=404, detail="Asset type not found")

    # 构建基础查询
    base_query = db.query(YieldStat).join(Token).join(Chain).join(AssetType)

    # 添加过滤条件
    filters = [
        Chain.id == chain.id,
        YieldStat.date == query.date,
        Token.asset_type_id == asset_type.id
    ]

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

    # 执行分页查询
    results = base_query.filter(and_(*filters)).offset(offset).limit(query.page_size).all()

    # 获取24小时数据
    yesterday = query.date - timedelta(days=1)
    yesterday_stats = {
        (stat.token_id, stat.return_type_id): stat
        for stat in base_query.filter(and_(
            Chain.id == chain.id,
            YieldStat.date == yesterday,
            Token.asset_type_id == asset_type.id
        )).all()
    }
    
    response_data = []
    for yield_stat in results:
        # 获取24小时统计数据
        yesterday_stat = yesterday_stats.get((yield_stat.token_id, yield_stat.return_type_id))
        
        token = yield_stat.token
        response_data.append({
            "token": token.symbol,
            "apy": yield_stat.apy,
            "tvl_usd": yield_stat.tvl_usd,
            "price_usd": token.price_usd,
            "chain": chain.name,
            "return_type": yield_stat.return_type.name,
            "vol_24h_usd": yesterday_stat.volume_usd if yesterday_stat else 0,
            "txns_24h": yesterday_stat.txns_count if yesterday_stat else 0,
            "asset_type": asset_type.name,
            "date": yield_stat.date
        })

    return {
        "data": response_data,
        "total": total_records,
        "page": query.page,
        "page_size": query.page_size,
        "total_pages": total_pages,
        "has_next": query.page < total_pages,
        "has_prev": query.page > 1
    }
