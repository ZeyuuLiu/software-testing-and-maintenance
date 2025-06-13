# -*- coding: utf-8 -*-
"""
功能：对单个 CSV 文件执行以下处理
    1. 缺失值填充：对除时间戳之外的所有特征列，使用“列均值”填充缺失值
    2. Min–Max 归一化：将所有数值型特征缩放到 [0, 1]
    3. 行号 104~116（含）为故障样本（label = 1），再从其前面同样数量的行中抽取正常样本（label = 0），两者合并为测试集
    4. 剩余行作为训练候选集，并对其进行 IQR 异常检测，剔除所有异常行，得到训练集
    5. 保存：
       - {output_prefix}_train.csv：训练集（时间戳 + 所有归一化特征，无标签，已剔除异常行）
       - {output_prefix}_test.csv ：测试集（时间戳 + 所有归一化特征 + 一列 label，包含故障与正常样本）

参数：
    input_csv_path (str)：待处理 CSV 文件路径
    output_prefix    (str)：输出文件名前缀（不包含后缀）
    timestamp_col    (str or None)：时间戳列的列名；若为 None，则自动使用 CSV 的第一列
    epsilon          (float)：筛选有效特征时 IQR 的下限阈值，默认 1e-6
    k                (float)：IQR 异常检测的放大系数，默认 1.5
"""

import os
import pandas as pd

def preprocess_with_row_split(
    input_csv_path: str,
    output_prefix: str,
    timestamp_col: str = None,
    epsilon: float = 1e-6,
    k: float = 1.5
):
    # 1. 读取 CSV 并自动识别表头
    df = pd.read_csv(input_csv_path, encoding='utf-8')

    # 2. 如果未指定时间戳列名，就默认用第一列
    if timestamp_col is None:
        timestamp_col = df.columns[0]

    # 3. 将时间戳列单独取出，其余列视为数值型特征
    timestamps = df[timestamp_col]
    features   = df.drop(columns=[timestamp_col])

    # 4. 对每个特征列先填充缺失值（用列均值），再做 Min–Max 归一化
    norm_feats = pd.DataFrame(index=features.index)
    for col in features.columns:
        col_series = features[col]
        # 如果存在缺失值，则用该列均值填充
        if col_series.isnull().any():
            mean_val = col_series.mean()
            col_series = col_series.fillna(mean_val)
        # 计算最小值和最大值
        min_val = col_series.min()
        max_val = col_series.max()
        # 如果该列所有值相等或全为 NaN，就用 0；否则做 (x - min) / (max - min)
        if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
            normalized = col_series.apply(lambda x: 0.0)
        else:
            normalized = (col_series - min_val) / (max_val - min_val)
        norm_feats[col] = normalized

    # 5. 将归一化后的特征与时间戳合并，形成完整的 DataFrame
    processed_df = pd.concat(
        [timestamps.reset_index(drop=True), norm_feats.reset_index(drop=True)],
        axis=1
    )

    # 6. 指定行号 104~116（含）为故障数据，构成测试集中 label=1 的部分
    fault_indices = list(range(104, 117))  # loc 索引从 0 开始，对应第 105~117 行
    num_faults = len(fault_indices)

    # 7. 从故障区间前面同样数量的行中抽取“正常”测试样本，作为 label=0
    #    保证这段范围不会与故障区间重叠
    normal_indices = list(range(fault_indices[0] - num_faults, fault_indices[0]))
    # 在实际数据长度不够时，需提前检查
    if normal_indices[0] < 0:
        raise ValueError("normal_indices 超出范围，请调整取样逻辑或检查行数是否足够。")

    # 8. 构造测试集，将故障与正常样本合并
    test_fault_df = processed_df.loc[fault_indices].reset_index(drop=True).copy()
    test_fault_df['label'] = 1

    test_normal_df = processed_df.loc[normal_indices].reset_index(drop=True).copy()
    test_normal_df['label'] = 0

    test_df = pd.concat([test_normal_df, test_fault_df], axis=0).reset_index(drop=True)

    # 9. 剩余行作为训练候选集
    train_candidates = processed_df.drop(index=fault_indices + normal_indices).reset_index(drop=True)

    # 10. 在训练候选集上进行 IQR 异常检测，并剔除所有异常行
    feat_cols = [col for col in train_candidates.columns if col != timestamp_col]
    train_feats = train_candidates[feat_cols]

    # 10.1 计算 Q1, Q3, IQR
    Q1 = train_feats.quantile(0.25)
    Q3 = train_feats.quantile(0.75)
    IQR = Q3 - Q1

    # 10.2 筛选“有效特征”：仅保留 IQR > epsilon 的列
    valid_cols = [col for col in feat_cols if IQR[col] > epsilon]
    if not valid_cols:
        valid_cols = feat_cols.copy()

    # 10.3 计算有效特征的正常上下界
    lower_bound = Q1[valid_cols] - k * IQR[valid_cols]
    upper_bound = Q3[valid_cols] + k * IQR[valid_cols]

    # 10.4 判断训练候选集中哪些行是正常的：所有有效特征都在上下界之间
    def is_normal_row(row):
        too_low  = row < lower_bound
        too_high = row > upper_bound
        return not (too_low.any() or too_high.any())

    train_valid_feats = train_feats[valid_cols]
    mask_train_normal = train_valid_feats.apply(is_normal_row, axis=1)
    train_df = train_candidates[mask_train_normal].reset_index(drop=True)

    # 11. 确保输出目录存在
    output_dir = os.path.dirname(output_prefix)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 12. 保存训练集和测试集
    train_output_path = f"{output_prefix}_train.csv"
    test_output_path  = f"{output_prefix}_test.csv"

    # 训练集不含 label，仅包含时间戳和归一化特征
    train_df.to_csv(train_output_path, index=False, encoding='utf-8')
    print(f"训练集（已剔除异常行）已保存到：{train_output_path}")

    # 测试集包含时间戳、归一化特征和 label（含正常样本与故障样本）
    test_df.to_csv(test_output_path, index=False, encoding='utf-8')
    print(f"测试集（含正常和故障样本）已保存到：{test_output_path}")

    return train_df, test_df

if __name__ == "__main__":
    # 示例用法：
    input_path    = r"/Online-Boutique/data_process/tabel1.csv"
    output_prefix = r"D:\desk\software-testing-and-maintenance-main\Online-Boutique\data_processed"

    preprocess_with_row_split(
        input_path,
        output_prefix,
        timestamp_col="Time",
        epsilon=1e-6,
        k=1.5
    )
