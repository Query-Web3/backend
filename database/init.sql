-- 创建数据库
CREATE DATABASE IF NOT EXISTS queryweb3_front CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE queryweb3_front;

-- 1. 区块链网络表
CREATE TABLE IF NOT EXISTS dim_chains (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '网络名称，如 Polkadot、Kusama、Hydration、Bifrost',
    chain_id INT NOT NULL COMMENT '链ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '区块链网络信息表';

-- 2. 资产类型表
CREATE TABLE IF NOT EXISTS dim_asset_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '资产类型名称，如 DeFi、GameFi、NFT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_name (name)
) COMMENT '资产类型表';

-- 3. 收益类型表
CREATE TABLE IF NOT EXISTS dim_return_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '收益类型，如 Staking、Farming、Lending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_name (name)
) COMMENT '收益类型表';

-- 4. 代币表
CREATE TABLE IF NOT EXISTS dim_tokens (
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
CREATE TABLE IF NOT EXISTS fact_token_daily_stats (
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
CREATE TABLE IF NOT EXISTS fact_yield_stats (
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
CREATE TABLE IF NOT EXISTS dim_stat_cycles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL COMMENT '统计周期名称(daily/weekly/monthly/yearly)',
    days INT NOT NULL COMMENT '周期天数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_name (name)
) COMMENT '统计周期表';



-- 初始化基础数据
ALTER TABLE dim_stat_cycles
  ADD UNIQUE KEY (name);
	
INSERT IGNORE INTO dim_stat_cycles (name, days)
VALUES
    ('daily', 1),
    ('weekly', 7),
    ('monthly', 30),
    ('yearly', 365);


-- 确保 name 字段唯一
ALTER TABLE dim_asset_types
  ADD UNIQUE KEY (name);

-- 使用 INSERT IGNORE 插入多条记录
INSERT IGNORE INTO dim_asset_types (name)
VALUES
    ('DeFi'),
    ('GameFi'),
    ('NFT');


ALTER TABLE dim_return_types
  ADD UNIQUE KEY (name);

INSERT IGNORE INTO dim_return_types (name)
VALUES
    ('Staking'),
    ('Farming'),
    ('Lending');


-- 添加一些示例链
ALTER TABLE dim_chains
  ADD UNIQUE KEY (name);

INSERT IGNORE INTO dim_chains (name)
VALUES
    ('Polkadot'),   
    ('Kusama'), 
    ('Hydration'),
    ('Bifrost');

-- 插入代币数据
INSERT INTO dim_tokens
(id, chain_id, address, symbol, name, decimals, asset_type_id)
VALUES
(1, 3, '0x1234567890123456789012345678901234567890', 'TKN1', 'Token1', 18, 1),
(2, 3, '0x2345678901234567890123456789012345678901', 'TKN2', 'Token2', 18, 1),
(3, 3, '0x3456789012345678901234567890123456789012', 'TKN3', 'Token3', 18, 1),
(4, 3, '0x4567890123456789012345678901234567890123', 'TKN4', 'Token4', 18, 1),
(5, 3, '0x5678901234567890123456789012345678901234', 'TKN5', 'Token5', 18, 1);

INSERT INTO fact_token_daily_stats
(token_id, date, volume, volume_usd, txns_count, price_usd, volume_yoy, volume_qoq, txns_yoy)
WITH RECURSIVE dates AS (
    SELECT CURDATE() - INTERVAL 100 DAY as date
    UNION ALL
    SELECT date + INTERVAL 1 DAY
    FROM dates
    WHERE date < CURDATE()
)
SELECT
    1 as token_id,
    d.date,
    ROUND(RAND() * 1000000, 4) as volume,
    ROUND(RAND() * 1000000, 4) as volume_usd,
    FLOOR(RAND() * 100000) as txns_count,
    ROUND(RAND() * 1000, 4) as price_usd,
    ROUND((RAND() * 20 - 10), 2) as volume_yoy,
    ROUND((RAND() * 15 - 7), 2) as volume_qoq,
    ROUND((RAND() * 30 - 15), 2) as txns_yoy
FROM dates d;


INSERT INTO fact_yield_stats
(token_id, return_type_id, pool_address, date, apy, tvl, tvl_usd)
WITH RECURSIVE dates AS (
    SELECT CURDATE() - INTERVAL 49 DAY as date
    UNION ALL
    SELECT date + INTERVAL 1 DAY
    FROM dates
    WHERE date < CURDATE()
),
tokens AS (
    SELECT 1 as token_id UNION ALL
    SELECT 2 UNION ALL
    SELECT 3 UNION ALL
    SELECT 4 UNION ALL
    SELECT 5
),
pools AS (
    SELECT
        t.token_id,
        CONCAT('0x', LPAD(HEX(t.token_id * 1000 + ROW_NUMBER() OVER (PARTITION BY t.token_id ORDER BY t.token_id)), 40, '0')) as pool_address
    FROM tokens t
    CROSS JOIN (SELECT 1 as n UNION ALL SELECT 2) numbers
)
SELECT
    p.token_id,
    1 + FLOOR(RAND() * 3) as return_type_id,  -- 随机生成1-3的return_type_id
    p.pool_address,
    d.date,
    ROUND(RAND() * 20, 2) as apy,             -- 0-20% 的 APY
    ROUND(RAND() * 1000000, 4) as tvl,        -- 保留4位小数的 TVL
    ROUND(RAND() * 1000000, 4) as tvl_usd     -- 保留4位小数的 TVL USD
FROM dates d
CROSS JOIN pools p
ORDER BY RAND()
LIMIT 250