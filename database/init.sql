/*
 Navicat Premium Data Transfer

 Source Server         : queryweb3
 Source Server Type    : MySQL
 Source Server Version : 80041
 Source Host           : 194.233.75.155:3306
 Source Schema         : queryweb3_front

 Target Server Type    : MySQL
 Target Server Version : 80041
 File Encoding         : 65001

 Date: 05/05/2025 11:05:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dim_asset_types
-- ----------------------------
DROP TABLE IF EXISTS `dim_asset_types`;
CREATE TABLE `dim_asset_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '资产类型名称，如 DeFi、GameFi、NFT',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='资产类型表';

-- ----------------------------
-- Table structure for dim_chains
-- ----------------------------
DROP TABLE IF EXISTS `dim_chains`;
CREATE TABLE `dim_chains` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '网络名称，如 Polkadot、Kusama、Hydration、Bifrost',
  `chain_id` int NOT NULL COMMENT '链ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='区块链网络信息表';

-- ----------------------------
-- Table structure for dim_return_types
-- ----------------------------
DROP TABLE IF EXISTS `dim_return_types`;
CREATE TABLE `dim_return_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '收益类型，如 Staking、Farming、Lending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='收益类型表';

-- ----------------------------
-- Table structure for dim_stat_cycles
-- ----------------------------
DROP TABLE IF EXISTS `dim_stat_cycles`;
CREATE TABLE `dim_stat_cycles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL COMMENT '统计周期名称(daily/weekly/monthly/yearly)',
  `days` int NOT NULL COMMENT '周期天数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='统计周期表';

-- ----------------------------
-- Table structure for dim_tokens
-- ----------------------------
DROP TABLE IF EXISTS `dim_tokens`;
CREATE TABLE `dim_tokens` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chain_id` int NOT NULL COMMENT '所属链ID',
  `address` varchar(42) NOT NULL COMMENT '代币合约地址',
  `symbol` varchar(20) NOT NULL COMMENT '代币符号',
  `name` varchar(100) NOT NULL COMMENT '代币名称',
  `decimals` int NOT NULL COMMENT '精度',
  `asset_type_id` int NOT NULL COMMENT '资产类型ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_token` (`chain_id`,`address`)
) ENGINE=InnoDB AUTO_INCREMENT=767102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代币基础信息表';

-- ----------------------------
-- Table structure for etl_control
-- ----------------------------
DROP TABLE IF EXISTS `etl_control`;
CREATE TABLE `etl_control` (
  `task_name` varchar(100) NOT NULL,
  `last_run` datetime DEFAULT NULL,
  PRIMARY KEY (`task_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for fact_token_daily_stats
-- ----------------------------
DROP TABLE IF EXISTS `fact_token_daily_stats`;
CREATE TABLE `fact_token_daily_stats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token_id` int NOT NULL COMMENT '代币ID',
  `date` date NOT NULL COMMENT '日期',
  `volume` decimal(65,18) NOT NULL COMMENT '交易量',
  `volume_usd` decimal(65,18) NOT NULL COMMENT 'USD交易量',
  `txns_count` int NOT NULL COMMENT '交易笔数',
  `price_usd` decimal(36,18) NOT NULL COMMENT 'USD价格',
  `volume_yoy` decimal(65,18) DEFAULT NULL COMMENT '交易量同比增长率(%)',
  `volume_qoq` decimal(65,18) DEFAULT NULL COMMENT '交易量环比增长率(%)',
  `txns_yoy` decimal(10,2) DEFAULT NULL COMMENT '交易数同比增长率(%)',
  `txns_qoq` decimal(10,2) DEFAULT NULL COMMENT '交易数环比增长率(%)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `unique_daily_stats` (`token_id`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=122605 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代币每日统计数据表';

-- ----------------------------
-- Table structure for fact_token_monthly_stats
-- ----------------------------
DROP TABLE IF EXISTS `fact_token_monthly_stats`;
CREATE TABLE `fact_token_monthly_stats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token_id` int NOT NULL COMMENT '代币ID',
  `date` date NOT NULL COMMENT '日期',
  `volume` decimal(65,18) NOT NULL COMMENT '交易量',
  `volume_usd` decimal(65,18) NOT NULL COMMENT 'USD交易量',
  `txns_count` int NOT NULL COMMENT '交易笔数',
  `price_usd` decimal(36,18) NOT NULL COMMENT 'USD价格',
  `volume_yoy` decimal(65,18) DEFAULT NULL COMMENT '交易量同比增长率(%)',
  `volume_qoq` decimal(65,18) DEFAULT NULL COMMENT '交易量环比增长率(%)',
  `txns_yoy` decimal(10,2) DEFAULT NULL COMMENT '交易数同比增长率(%)',
  `txns_qoq` decimal(10,2) DEFAULT NULL COMMENT '交易数环比增长率(%)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `unique_daily_stats` (`token_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代币每日统计数据表';

-- ----------------------------
-- Table structure for fact_token_weekly_stats
-- ----------------------------
DROP TABLE IF EXISTS `fact_token_weekly_stats`;
CREATE TABLE `fact_token_weekly_stats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token_id` int NOT NULL COMMENT '代币ID',
  `date` date NOT NULL COMMENT '日期',
  `volume` decimal(65,18) NOT NULL COMMENT '交易量',
  `volume_usd` decimal(65,18) NOT NULL COMMENT 'USD交易量',
  `txns_count` int NOT NULL COMMENT '交易笔数',
  `price_usd` decimal(36,18) NOT NULL COMMENT 'USD价格',
  `volume_yoy` decimal(65,18) DEFAULT NULL COMMENT '交易量同比增长率(%)',
  `volume_qoq` decimal(65,18) DEFAULT NULL COMMENT '交易量环比增长率(%)',
  `txns_yoy` decimal(10,2) DEFAULT NULL COMMENT '交易数同比增长率(%)',
  `txns_qoq` decimal(10,2) DEFAULT NULL COMMENT '交易数环比增长率(%)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `unique_daily_stats` (`token_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代币每日统计数据表';

-- ----------------------------
-- Table structure for fact_token_yearly_stats
-- ----------------------------
DROP TABLE IF EXISTS `fact_token_yearly_stats`;
CREATE TABLE `fact_token_yearly_stats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token_id` int NOT NULL COMMENT '代币ID',
  `date` date NOT NULL COMMENT '日期',
  `volume` decimal(65,18) NOT NULL COMMENT '交易量',
  `volume_usd` decimal(65,18) NOT NULL COMMENT 'USD交易量',
  `txns_count` int NOT NULL COMMENT '交易笔数',
  `price_usd` decimal(36,18) NOT NULL COMMENT 'USD价格',
  `volume_yoy` decimal(65,18) DEFAULT NULL COMMENT '交易量同比增长率(%)',
  `volume_qoq` decimal(65,18) DEFAULT NULL COMMENT '交易量环比增长率(%)',
  `txns_yoy` decimal(10,2) DEFAULT NULL COMMENT '交易数同比增长率(%)',
  `txns_qoq` decimal(10,2) DEFAULT NULL COMMENT '交易数环比增长率(%)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `unique_daily_stats` (`token_id`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代币每日统计数据表';

-- ----------------------------
-- Table structure for fact_yield_stats
-- ----------------------------
DROP TABLE IF EXISTS `fact_yield_stats`;
CREATE TABLE `fact_yield_stats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token_id` int NOT NULL COMMENT '代币ID',
  `return_type_id` int NOT NULL COMMENT '收益类型ID',
  `pool_address` varchar(42) NOT NULL COMMENT '流动池地址',
  `date` date NOT NULL COMMENT '日期',
  `apy` decimal(10,2) NOT NULL COMMENT '年化收益率(%)',
  `tvl` decimal(65,18) NOT NULL COMMENT '总锁仓量',
  `tvl_usd` decimal(65,18) NOT NULL COMMENT 'USD总锁仓量',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_daily_yield` (`token_id`,`pool_address`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=118056 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='收益率数据表';

SET FOREIGN_KEY_CHECKS = 1;
