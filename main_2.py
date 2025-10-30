import pandas as pd
import os
import numpy as np

# 读取 countdf
countdf = pd.read_csv("count_df.csv", index_col=0)
meandf = pd.read_csv("mean.csv")

# 训练集文件夹
train_folder = r"F:\项目\lstm1\train_data"
train_files = [os.path.join(train_folder, f) for f in os.listdir(train_folder)]

# 遍历阈值 n
best_n = 0
best_w1 = 0
best_acc = 0
best_w2 = 0
day = 3

# 遍历阈值 n 和 权重 w1
for n in np.arange(0.68, 0.71, 0.01):
    for w_1 in np.arange(-11, -0.5, 1):  # mean 的权重
        for w_2 in np.arange(-9, 6 , 2) :
            correct = 0
            total = 0

            for file in train_files:
                df = pd.read_csv(file)
                for _, row in df.iterrows():
                    maturity = int(row['maturity'])
                    maturity_str = str(maturity)
                    if maturity_str not in countdf.columns:
                        continue
                    
                    adj_mean = 0
                    count = 0
                    for i in range(day+1):  # 包含今天
                        m = maturity - i
                        if m in meandf.index:
                            mean_val = meandf.loc[m].values[1]
                            adj_mean += mean_val
                            count += 1
                    if count > 0:
                        adj_mean /= count  # 平均

                    up = countdf.at['up', maturity_str]
                    down = countdf.at['down', maturity_str]

                    # 找对应均值
                    if int(maturity) not in meandf.index:
                        continue
                    mean = meandf.loc[int(maturity)].values[1]

                    if up + down == 0:
                        continue

                    # 计算上涨概率 + 调整
                    p_up = up / (up + down)
                    adj_p = p_up + w_1 * mean + w_2 * adj_mean

                    # 根据调整后的概率预测
                    if adj_p > n:
                        prediction = 1
                    elif adj_p < 1 - n :
                        prediction = -1
                    else :
                        continue

                    # 实际涨跌
                    if row['change'] > 0:
                        actual = 1
                    elif row['change'] < 0 :
                        actual = -1
                    else :
                        continue

                    total += 1
                    if prediction == actual:
                        correct += 1

            if total > 0:
                acc = correct / total
                if acc > best_acc:
                    print(f"change: n = {n:.4f}, w_1 = {w_1:.4f}, w_2 = {w_2:.4f}")
                    best_acc = acc
                    best_n = n
                    best_w1 = w_1
                    best_w2 = w_2


print(f"最佳准确率: {best_acc:.4f}")
print(f"最佳参数: n = {best_n:.4f}, w_1 = {best_w1:.4f}, w_2 = {best_w2:.4f}")
