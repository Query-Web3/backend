from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from decimal import Decimal

# Base Schemas
class ChainBase(BaseModel):
    name: str
    chain_id: int

class TokenBase(BaseModel):
    symbol: str
    chain: str

# Request Schemas
class VolTxnsQuery(BaseModel):
    from_date: date
    to_date: date
    chain: str
    cycle: str

class YieldQuery(BaseModel):
    date: date
    chain: str
    asset_type: str
    return_type: Optional[str] = None
    token: Optional[str] = None

# Response Schemas
class VolTxnsResponse(BaseModel):
    time: date
    volume: Decimal
    yoy: Optional[Decimal]
    qoq: Optional[Decimal]
    txns: int
    txns_yoy: Optional[Decimal]

class YieldResponse(BaseModel):
    token: str
    apy: Decimal
    tvl_usd: Decimal
    price_usd: Decimal
    chain: str
    return_type: str
    vol_24h_usd: Decimal
    txns_24h: int
    asset_type: str
    date: date

class VolTxnsListResponse(BaseModel):
    data: List[VolTxnsResponse]
    total: int

class YieldListResponse(BaseModel):
    data: List[YieldResponse]
    total: int
