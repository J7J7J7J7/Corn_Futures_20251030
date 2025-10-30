import os
import pandas as pd
from datetime import datetime

# === 配置部分 ===
input_folder = r"F:\项目\lstm1\corn_futures"       # 原始数据文件夹
output_folder = r"F:/项目/lstm1/corn_processed" # 输出保存文件夹

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

df_basic = pd.read_csv("F:/项目/lstm1/basic.csv")
# === 遍历所有 csv 文件 ===
for filename in os.listdir(input_folder):
    if not filename.endswith(".csv"):
        continue

    file_path = os.path.join(input_folder, filename)
    df = pd.read_csv(file_path)
    # ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,change1,change2,vol,amount,oi,oi_chg
    # ts_code,symbol,name,list_date,delist_date
    # === 基本字段检查 ===
    if 'trade_date' not in df.columns or 'close' not in df.columns :
        print(f" 跳过文件（缺少必要字段）: {filename}")
        continue
    
    delist_date = df_basic.loc[df['ts_code'][0] == df_basic['ts_code'], 'delist_date']
    delist_date = pd.to_datetime(delist_date, format = '%Y%m%d')
    delist_date = delist_date.values[0]
    # === 日期格式处理 ===
    df['trade_date'] = pd.to_datetime(df['trade_date'], format = '%Y%m%d')
    # === 计算价格变化率（涨跌百分比）===
    df['change'] = df['settle'] / df['pre_settle'] - 1 # 转为百分比

    # === 计算距离到期日（天）===
    df['maturity'] = (delist_date - df['trade_date']).dt.days


    # === 保存到新文件夹 ===
    output_path = os.path.join(output_folder, filename)
    df.to_csv(output_path, index=False)

    print(f"已处理并保存: {filename}")
