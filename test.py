import pandas as pd
import os

# 读取 countdf
countdf = pd.read_csv("count_df.csv", index_col=0)
meandf = pd.read_csv("mean.csv")
# 测试集文件夹
test_folder = r"F:\项目\lstm1\test_data"

total = 0
correct = 0

# 使用在训练阶段找到的最优参数
n = 0.69
w_1 = -5
w_2 = -3
day = 3
for file in os.listdir(test_folder):
    if file.endswith(".csv"):
        df_test = pd.read_csv(os.path.join(test_folder, file))
        
        for _, row in df_test.iterrows():
            maturity = int(row['maturity'])
            maturity_str = str(maturity)

            # 检查是否存在该 maturity
            if maturity_str not in countdf.columns or maturity not in meandf.index:
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

            if up + down == 0:
                continue

            mean = meandf.loc[maturity].values[1]

            # 调整后的概率
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

accuracy = correct / total
print(f"预测准确率: {accuracy:.4f}")
