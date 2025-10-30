import tushare as ts
import pandas as pd

# 初始化
pro = ts.pro_api('Token')

# 获取大连商品交易所玉米合约信息
df_contracts = pro.fut_basic(exchange='DCE', fut_type='1')  # '1' 表示商品期货

# 过滤出玉米（C）合约
df_contracts = df_contracts[df_contracts['ts_code'].str.match(r'^C\d{4}\.DCE$')]

# 选取关键字段
df_contracts = df_contracts[['ts_code', 'symbol', 'name', 'list_date', 'delist_date']]
df_contracts = df_contracts.sort_values('list_date').reset_index(drop=True)
df_contracts.to_csv("basic.csv", index=False, encoding='utf-8-sig')
print(df_contracts.head())
