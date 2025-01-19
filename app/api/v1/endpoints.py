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

    # 执行查询
    results = base_query.filter(and_(*filters)).all()

    # 获取24小时数据
    yesterday = query.date - timedelta(days=1)
    
    response_data = []
    for yield_stat in results:
        # 获取24小时统计数据
        daily_stat = db.query(TokenDailyStat).filter(
            and_(
                TokenDailyStat.token_id == yield_stat.token_id,
                TokenDailyStat.date == yesterday
            )
        ).first()

        response_data.append({
            "token": yield_stat.token.symbol,
            "apy": yield_stat.apy,
            "tvl_usd": yield_stat.tvl_usd,
            "price_usd": daily_stat.price_usd if daily_stat else 0,
            "chain": chain.name,
            "return_type": yield_stat.return_type.name,
            "vol_24h_usd": daily_stat.volume_usd if daily_stat else 0,
            "txns_24h": daily_stat.txns_count if daily_stat else 0,
            "asset_type": asset_type.name,
            "date": yield_stat.date
        })

    return {
        "data": response_data,
        "total": len(response_data)
    }
