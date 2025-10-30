import pandas as pd
import os

# === 文件夹路径 ===
folder_path = r"F:\项目\lstm1\train_data"   # 改成你的文件夹路径
save_path = r"F:\项目\lstm1\maturity.csv"

# 存放所有合约数据
all_data = []

# === 遍历文件夹 ===
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)

        df = df[['ts_code', 'maturity', 'change']].dropna()
        all_data.append(df)

# === 合并成一个 DataFrame ===
if all_data:
    result = pd.concat(all_data, ignore_index=True)
    result = result.sort_values(['ts_code', 'maturity'], ascending=[True, False])
    result.to_csv(save_path, index=False)
    print(f"✅ 已保存合并文件：{save_path}")
else:
    print("❌ 未找到有效数据。")