import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV，第一列是 ts_code
df = pd.read_csv("maturity_1.csv", index_col=0)

# 将列全部转换为浮点数，忽略空值
df = df.astype(float)

# 对每一行求平均值（忽略 NaN）
mean = df.mean(axis=0)
mean = mean.T
# 查看结果
print(mean)
x = mean.index[::-1]  # 366 到 0
y = mean.values[::-1]

def count_up_down(series):
    up = (series > 0).sum()
    down = (series < 0).sum()
    zero = (series == 0).sum()
    nan = series.isna().sum()
    return pd.Series([up, down, zero, nan], index=['up', 'down', 'zero', 'nan'])

# 对每一列应用
count_df = df.apply(count_up_down, axis=0)
print(count_df)
mean.to_csv("mean.csv")
count_df.to_csv("count_df.csv")
plt.figure(figsize=(12, 6))
plt.plot(x, y, marker='o', linestyle='-')
plt.xlabel("Days to Maturity")
plt.ylabel("Average Change")
plt.title("Average Daily Change Before Maturity")
plt.grid(True)
plt.gca().invert_xaxis()  
plt.xticks(x[::9])
plt.show()