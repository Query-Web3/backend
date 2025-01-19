-- 创建数据库
CREATE DATABASE IF NOT EXISTS queryweb3 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE queryweb3;

-- 1. 区块链网络表
CREATE TABLE IF NOT EXISTS chains (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '网络名称，如 Ethereum、BSC等',
    chain_id INT NOT NULL COMMENT '链ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '区块链网络信息表';

-- 2. 资产类型表
CREATE TABLE IF NOT EXISTS asset_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '资产类型名称，如 DeFi、GameFi等',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_name (name)
) COMMENT '资产类型表';

-- 3. 收益类型表
CREATE TABLE IF NOT EXISTS return_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '收益类型，如 Staking、Farming等',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_name (name)
) COMMENT '收益类型表';

-- 4. 代币表
CREATE TABLE IF NOT EXISTS tokens (
    id INT PRIMARY KEY AUTO_INCREMENT,
    chain_id INT NOT NULL COMMENT '所属链ID',
    address VARCHAR(42) NOT NULL COMMENT '代币合约地址',
    symbol VARCHAR(20) NOT NULL COMMENT '代币符号',
    name VARCHAR(100) NOT NULL COMMENT '代币名称',
    decimals INT NOT NULL COMMENT '精度',
    asset_type_id INT NOT NULL COMMENT '资产类型ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_token (chain_id, address)
) COMMENT '代币基础信息表';

-- 5. 代币每日数据表
CREATE TABLE IF NOT EXISTS token_daily_stats (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    token_id INT NOT NULL COMMENT '代币ID',
    date DATE NOT NULL COMMENT '日期',
    volume DECIMAL(36,18) NOT NULL COMMENT '交易量',
    volume_usd DECIMAL(36,18) NOT NULL COMMENT 'USD交易量',
    txns_count INT NOT NULL COMMENT '交易笔数',
    price_usd DECIMAL(36,18) NOT NULL COMMENT 'USD价格',
    volume_yoy DECIMAL(10,2) DEFAULT NULL COMMENT '交易量同比增长率(%)',
    volume_qoq DECIMAL(10,2) DEFAULT NULL COMMENT '交易量环比增长率(%)',
    txns_yoy DECIMAL(10,2) DEFAULT NULL COMMENT '交易数同比增长率(%)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_daily_stats (token_id, date)
) COMMENT '代币每日统计数据表';

-- 6. 收益率数据表
CREATE TABLE IF NOT EXISTS yield_stats (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    token_id INT NOT NULL COMMENT '代币ID',
    return_type_id INT NOT NULL COMMENT '收益类型ID',
    pool_address VARCHAR(42) NOT NULL COMMENT '流动池地址',
    date DATE NOT NULL COMMENT '日期',
    apy DECIMAL(10,2) NOT NULL COMMENT '年化收益率(%)',
    tvl DECIMAL(36,18) NOT NULL COMMENT '总锁仓量',
    tvl_usd DECIMAL(36,18) NOT NULL COMMENT 'USD总锁仓量',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_daily_yield (token_id, pool_address, date)
) COMMENT '收益率数据表';

-- 7. 统计周期表
CREATE TABLE IF NOT EXISTS stat_cycles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL COMMENT '统计周期名称(daily/weekly/monthly/yearly)',
    days INT NOT NULL COMMENT '周期天数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_name (name)
) COMMENT '统计周期表';

-- 初始化基础数据
ALTER TABLE stat_cycles
  ADD UNIQUE KEY (name);
	
INSERT IGNORE INTO stat_cycles (name, days)
VALUES
    ('daily', 1),
    ('weekly', 7),
    ('monthly', 30),
    ('yearly', 365);


-- 确保 name 字段唯一
ALTER TABLE asset_types
  ADD UNIQUE KEY (name);

-- 使用 INSERT IGNORE 插入多条记录
INSERT IGNORE INTO asset_types (name)
VALUES
    ('DeFi'),
    ('GameFi'),
    ('NFT');


ALTER TABLE return_types
  ADD UNIQUE KEY (name);

INSERT IGNORE INTO return_types (name)
VALUES
    ('Staking'),
    ('Farming'),
    ('Lending');


-- 添加一些示例链
ALTER TABLE chains
  ADD UNIQUE KEY (name);

INSERT IGNORE INTO chains (name)
VALUES
    ('Polkadot'),   
    ('Kusama'), 
    ('Hydration'),
    ('Bifrost');
