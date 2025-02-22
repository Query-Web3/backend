import pymysql
from datetime import datetime, timedelta
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'queryweb3',
    'charset': 'utf8mb4'
}

def check_yield_dates():
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cursor:
            # 查询所有可用的日期
            cursor.execute("""
                SELECT DISTINCT date 
                FROM fact_yield_stats 
                ORDER BY date
            """)
            dates = cursor.fetchall()
            
            if not dates:
                print("\n没有找到任何收益率数据。")
                return

            print("\n可用的日期:")
            for (date,) in dates:
                print(f"- {date}")

            # 获取一个示例数据
            cursor.execute("""
                SELECT 
                    ys.date,
                    t.symbol,
                    c.name as chain,
                    at.name as asset_type,
                    rt.name as return_type,
                    ys.apy,
                    ys.tvl_usd
                FROM fact_yield_stats ys
                JOIN dim_tokens t ON t.id = ys.token_id
                JOIN dim_chains c ON c.id = t.chain_id
                JOIN dim_asset_types at ON at.id = t.asset_type_id
                JOIN dim_return_types rt ON rt.id = ys.return_type_id
                LIMIT 1
            """)
            sample = cursor.fetchone()

            if sample:
                print("\n示例数据:")
                print(f"日期: {sample[0]}")
                print(f"代币: {sample[1]}")
                print(f"链: {sample[2]}")
                print(f"资产类型: {sample[3]}")
                print(f"收益类型: {sample[4]}")
                print(f"APY: {sample[5]}%")
                print(f"TVL(USD): ${sample[6]:,.2f}")

            # 查询数据总量
            cursor.execute("SELECT COUNT(*) FROM fact_yield_stats")
            total = cursor.fetchone()[0]
            print(f"\n总记录数: {total}")

    finally:
        conn.close()

def check_specific_date():
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cursor:
            # 查询特定日期的数据
            specific_date = '2024-12-06'
            cursor.execute("""
                SELECT 
                    ys.date,
                    t.symbol,
                    c.name as chain,
                    at.name as asset_type,
                    rt.name as return_type,
                    ys.apy,
                    ys.tvl_usd
                FROM fact_yield_stats ys
                JOIN dim_tokens t ON t.id = ys.token_id
                JOIN dim_chains c ON c.id = t.chain_id
                JOIN dim_asset_types at ON at.id = t.asset_type_id
                JOIN dim_return_types rt ON rt.id = ys.return_type_id
                WHERE ys.date = %s
                AND t.symbol = 'TKN1'
                AND c.name = 'Hydration'
                AND at.name = 'DeFi'
                AND rt.name = 'Staking'
            """, (specific_date,))
            
            results = cursor.fetchall()
            
            print(f"\n查询条件:")
            print(f"日期: {specific_date}")
            print("代币: TKN1")
            print("链: Hydration")
            print("资产类型: DeFi")
            print("收益类型: Staking")
            
            if not results:
                print("\n没有找到符合条件的数据")
                
                # 查询最近的可用日期
                cursor.execute("""
                    SELECT MIN(date), MAX(date)
                    FROM fact_yield_stats
                """)
                min_date, max_date = cursor.fetchone()
                print(f"\n数据库中的日期范围:")
                print(f"最早日期: {min_date}")
                print(f"最晚日期: {max_date}")
            else:
                print("\n查询结果:")
                for row in results:
                    print(f"日期: {row[0]}")
                    print(f"代币: {row[1]}")
                    print(f"链: {row[2]}")
                    print(f"资产类型: {row[3]}")
                    print(f"收益类型: {row[4]}")
                    print(f"APY: {row[5]}%")
                    print(f"TVL(USD): ${row[6]:,.2f}")

    finally:
        conn.close()

if __name__ == "__main__":
    check_yield_dates()
    check_specific_date()
