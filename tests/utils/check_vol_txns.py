import pymysql
from datetime import datetime, timedelta

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'queryweb3',
    'charset': 'utf8mb4'
}

def check_vol_txns_data():
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cursor:
            # 1. 查询可用的链
            cursor.execute("""
                SELECT DISTINCT c.name
                FROM dim_chains c
                JOIN dim_tokens t ON t.chain_id = c.id
                JOIN fact_token_daily_stats s ON s.token_id = t.id
            """)
            chains = [row[0] for row in cursor.fetchall()]
            print("\n可用的链:")
            for chain in chains:
                print(f"- {chain}")

            # 2. 查询数据的日期范围
            cursor.execute("""
                SELECT MIN(date), MAX(date)
                FROM fact_token_daily_stats
            """)
            min_date, max_date = cursor.fetchone()
            print(f"\n数据日期范围:")
            print(f"最早日期: {min_date}")
            print(f"最晚日期: {max_date}")

            # 3. 查询可用的统计周期
            cursor.execute("SELECT name, days FROM dim_stat_cycles")
            cycles = cursor.fetchall()
            print("\n可用的统计周期:")
            for cycle, days in cycles:
                print(f"- {cycle} ({days}天)")

            # 4. 查询一个示例数据
            cursor.execute("""
                SELECT 
                    s.date,
                    c.name as chain,
                    t.symbol,
                    s.volume,
                    s.volume_usd,
                    s.txns_count,
                    s.volume_yoy,
                    s.volume_qoq,
                    s.txns_yoy
                FROM fact_token_daily_stats s
                JOIN dim_tokens t ON t.id = s.token_id
                JOIN dim_chains c ON c.id = t.chain_id
                WHERE s.volume > 0
                LIMIT 1
            """)
            sample = cursor.fetchone()
            
            if sample:
                print("\n示例数据:")
                print(f"日期: {sample[0]}")
                print(f"链: {sample[1]}")
                print(f"代币: {sample[2]}")
                print(f"交易量: {float(sample[3]):,.2f}")
                print(f"USD交易量: ${float(sample[4]):,.2f}")
                print(f"交易笔数: {sample[5]}")
                print(f"交易量同比增长: {float(sample[6]):,.2f}%" if sample[6] else "交易量同比增长: N/A")
                print(f"交易量环比增长: {float(sample[7]):,.2f}%" if sample[7] else "交易量环比增长: N/A")
                print(f"交易数同比增长: {float(sample[8]):,.2f}%" if sample[8] else "交易数同比增长: N/A")

            # 5. 生成推荐的请求参数
            print("\n推荐的请求参数:")
            print("""
{
    "from_date": "%s",
    "to_date": "%s",
    "chain": "%s",
    "cycle": "daily"
}
            """ % (min_date, max_date, chains[0] if chains else ""))

    finally:
        conn.close()

if __name__ == "__main__":
    check_vol_txns_data()
