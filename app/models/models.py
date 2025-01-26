from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Chain(Base):
    __tablename__ = "dim_chains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    chain_id = Column(Integer, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class AssetType(Base):
    __tablename__ = "dim_asset_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

class ReturnType(Base):
    __tablename__ = "dim_return_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

class Token(Base):
    __tablename__ = "dim_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    chain_id = Column(Integer, nullable=False)
    address = Column(String(42), nullable=False)
    symbol = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    decimals = Column(Integer, nullable=False)
    asset_type_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class TokenDailyStat(Base):
    __tablename__ = "fact_token_daily_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    volume = Column(DECIMAL(36, 18), nullable=False)
    volume_usd = Column(DECIMAL(36, 18), nullable=False)
    txns_count = Column(Integer, nullable=False)
    price_usd = Column(DECIMAL(36, 18), nullable=False)
    volume_yoy = Column(DECIMAL(10, 2))
    volume_qoq = Column(DECIMAL(10, 2))
    txns_yoy = Column(DECIMAL(10, 2))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

class YieldStat(Base):
    __tablename__ = "fact_yield_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, nullable=False)
    return_type_id = Column(Integer, nullable=False)
    pool_address = Column(String(42), nullable=False)
    date = Column(Date, nullable=False)
    apy = Column(DECIMAL(10, 2), nullable=False)
    tvl = Column(DECIMAL(36, 18), nullable=False)
    tvl_usd = Column(DECIMAL(36, 18), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

class StatCycle(Base):
    __tablename__ = "dim_stat_cycles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, unique=True)
    days = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
