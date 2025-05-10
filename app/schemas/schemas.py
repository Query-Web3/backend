from pydantic import BaseModel, Field
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


# Pagination
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")


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
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")


# Response Schemas
class VolTxnsResponse(BaseModel):
    time: date
    volume: Decimal
    yoy: Optional[Decimal]
    qoq: Optional[Decimal]
    txns: int
    txns_yoy: Optional[Decimal]
    txns_qoq: Optional[Decimal]
    token: Optional[str] = None


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


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class VolTxnsListResponse(BaseModel):
    data: List[VolTxnsResponse]
    total: int


class YieldListResponse(PaginatedResponse):
    data: List[YieldResponse]
