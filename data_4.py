#划分测试集与训练集

import os
import shutil
import random

# 原始文件夹路径
source_folder = r"F:\项目\lstm1\corn_processed"

# 训练集和测试集文件夹
train_folder = r"F:\项目\lstm1\train_data"
test_folder = r"F:\项目\lstm1\test_data"

# 如果文件夹不存在就创建
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# 获取所有 CSV 文件
all_files = [f for f in os.listdir(source_folder) if f.endswith(".csv")]

# 随机打乱
random.shuffle(all_files)

# 按 8:2 划分
split_idx = int(len(all_files) * 0.8)
train_files = all_files[:split_idx]
test_files = all_files[split_idx:]

# 复制文件到目标文件夹
for f in train_files:
    shutil.copy(os.path.join(source_folder, f), os.path.join(train_folder, f))

for f in test_files:
    shutil.copy(os.path.join(source_folder, f), os.path.join(test_folder, f))

print(f"训练集: {len(train_files)} 个文件，测试集: {len(test_files)} 个文件")
