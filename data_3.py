import pandas as pd

# 读取数据
df = pd.read_csv("maturity.csv")  # 替换为你的文件名

# 确保数值列正确
df['maturity'] = pd.to_numeric(df['maturity'], errors='coerce')
df['change'] = pd.to_numeric(df['change'], errors='coerce')

# 创建透视表：ts_code × maturity，值为 change
df_pivot = df.pivot(index='ts_code', columns='maturity', values='change')

# 将 maturity 列按倒序排列
df_pivot = df_pivot.sort_index(axis=1, ascending=False)

# 保存为 CSV
df_pivot.to_csv("maturity_1.csv")

print(df_pivot.head())
