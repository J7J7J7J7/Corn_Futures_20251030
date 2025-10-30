# -*- coding: utf-8 -*-
"""
获取玉米期货各合约历史日线数据，并单独保存为 CSV
"""

import tushare as ts
import os

# -----------------------------
# 1. 初始化 Tushare
# -----------------------------
ts.set_token('3acaaa7a6d2096440993ab84701b7c1267d86ca2dde1f3964d118b3c')  # 替换为你的token
pro = ts.pro_api()

# -----------------------------
# 2. 创建保存目录
# -----------------------------
save_dir = 'corn_futures'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# -----------------------------
# 3. 获取玉米期货合约列表
# -----------------------------
def get_corn_contracts():
    df_contracts = pro.fut_basic(exchange='DCE', fut_type='1')  # 1=商品期货
    df_contracts = df_contracts[df_contracts['ts_code'].str.match(r'^C\d{4}\.DCE$')]
    df_contracts = df_contracts.sort_values('list_date')
    return df_contracts[['ts_code','name','list_date','delist_date']]

contracts_df = get_corn_contracts()
print("玉米期货合约列表：")
print(contracts_df)

# -----------------------------
# 4. 获取单个合约日线并保存
# -----------------------------
for idx, row in contracts_df.iterrows():
    ts_code = row['ts_code']
    name = row['name']
    start_date = row['list_date']
    end_date = row['delist_date']
    
    print(f"正在获取合约 {name} ({ts_code}) 数据...")
    try:
        df = pro.fut_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        df = df.sort_values('trade_date').reset_index(drop=True)
        
        file_path = os.path.join(save_dir, f"{ts_code}.csv")
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"保存完成: {file_path}")
    except Exception as e:
        print(f"获取合约 {ts_code} 数据失败: {e}")
