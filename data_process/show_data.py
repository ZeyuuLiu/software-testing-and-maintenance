import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 创建保存图片的文件夹
fig_dir = 'figures'
os.makedirs(fig_dir, exist_ok=True)

# 读取数据，记得改成你的文件路径
data_file = 'data_processed_train.csv'
df = pd.read_csv(data_file, parse_dates=['Time'])

# 选择几个关键指标列
cols = ['system_cpu_usage', 'user_cpu_usage', 'total_cpu_usage', 'load_1min', 'load_5min', 'load_15min']

# 设置画布大小和样式
sns.set(style="whitegrid")
fig, axes = plt.subplots(len(cols), 2, figsize=(12, 4*len(cols)))  # 每行2图，列数是指标数量，行高4

for i, col in enumerate(cols):
    # 左图：箱线图
    sns.boxplot(x=df[col], ax=axes[i, 0], color='skyblue')
    axes[i, 0].set_title(f'Boxplot of {col}')
    axes[i, 0].set_xlabel('')
    # 右图：核密度估计图
    sns.kdeplot(df[col], ax=axes[i, 1], shade=True, color='orange')
    axes[i, 1].set_title(f'Density Plot of {col}')
    axes[i, 1].set_xlabel('')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'key_metrics_distribution.png'))
plt.close()

print(f"多指标分布大图已保存到: {fig_dir}/key_metrics_distribution.png")



data_file = 'data_processed_test.csv'
df = pd.read_csv(data_file, parse_dates=['Time'])

cols = ['system_cpu_usage', 'user_cpu_usage', 'total_cpu_usage', 'load_1min', 'load_5min', 'load_15min']

sns.set(style="whitegrid")
fig, axes = plt.subplots(len(cols), 2, figsize=(12, 4*len(cols)))

for i, col in enumerate(cols):
    # 箱线图，按label区分颜色
    sns.boxplot(x='label', y=col, data=df, ax=axes[i, 0], palette='Set2')
    axes[i, 0].set_title(f'Boxplot of {col} by label')
    axes[i, 0].set_xlabel('label')
    axes[i, 0].set_ylabel(col)

    # 核密度图，分别绘制两类
    for label_val, color in zip([0,1], ['blue','red']):
        subset = df[df['label'] == label_val]
        sns.kdeplot(subset[col], ax=axes[i, 1], shade=True, color=color, label=f'label={label_val}')
    axes[i, 1].set_title(f'Density Plot of {col} by label')
    axes[i, 1].legend()
    axes[i, 1].set_xlabel(col)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'testset_metrics_distribution_by_label.png'))
plt.close()

print(f"测试集带标签颜色区分的大图已保存到: {fig_dir}/testset_metrics_distribution_by_label.png")