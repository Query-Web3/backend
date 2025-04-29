import requests
import json
from datetime import datetime

def test_vol_txns_request():
    url = "http://127.0.0.1:8000/api/v1/vol-txns"
    
    # 构造请求数据
    data = {
        "from_date": "2024-10-18",
        "to_date": "2025-01-26",
        "chain": "Hydration",
        "cycle": "daily"
    }
    
    # 发送请求
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        # 打印请求信息
        print("\n请求信息:")
        print(f"URL: {url}")
        print(f"Method: POST")
        print(f"Headers: {headers}")
        print(f"Request Body: {json.dumps(data, indent=2)}")
        
        # 打印响应信息
        print("\n响应信息:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n响应数据:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 打印数据统计
            if "data" in result:
                print(f"\n数据统计:")
                print(f"总记录数: {len(result['data'])}")
                print(f"日期范围: {result['data'][0]['time']} 到 {result['data'][-1]['time']}")
                
                # 计算总交易量和总交易数
                total_volume = sum(float(item['volume']) for item in result['data'])
                total_txns = sum(item['txns'] for item in result['data'])
                print(f"总交易量: {total_volume:,.2f}")
                print(f"总交易数: {total_txns:,}")
        else:
            print(f"错误响应: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

if __name__ == "__main__":
    test_vol_txns_request()
