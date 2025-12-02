# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 21:22:11 2025

@author: xiwangxiang
"""

import pandas as pd
import numpy as np
import os
import glob

def analyze_csv_files(directory='.'):
    """
    分析指定目录下所有CSV文件的缺失值情况
    
    参数:
    directory (str): 要分析的目录路径，默认为当前目录
    """
    # 获取所有CSV文件
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    
    if not csv_files:
        print("在当前目录下未找到CSV文件")
        return
    
    print(f"找到 {len(csv_files)} 个CSV文件\n")
    
    # 分析每个CSV文件
    for file_path in csv_files:
        print(f"分析文件: {os.path.basename(file_path)}")
        
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 检查缺失值
            total_missing = df.isnull().sum().sum()
            missing_by_column = df.isnull().sum()
            
            if total_missing == 0:
                print("  ✓ 无缺失值")
            else:
                print(f"  ⚠ 发现 {total_missing} 个缺失值")
                
                # 显示每列的缺失值情况
                print("  各列缺失值统计:")
                for col, count in missing_by_column.items():
                    if count > 0:
                        print(f"    - {col}: {count} 个缺失值 ({count/len(df)*100:.2f}%)")
                
                # 显示有缺失值的行
                missing_rows = df[df.isnull().any(axis=1)]
                print(f"  有缺失值的行数: {len(missing_rows)}")
                
                # 显示前几行有缺失值的样本
                if len(missing_rows) > 0:
                    print("  前5行有缺失值的样本:")
                    for idx, row in missing_rows.head().iterrows():
                        missing_cols = row.index[row.isnull()].tolist()
                        print(f"    第 {idx+1} 行: 缺失列 - {', '.join(missing_cols)}")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"  ✗ 读取文件时出错: {e}")
            print("-" * 50)

def main():
    """主函数"""
    print("开始分析CSV文件中的缺失值...\n")
    analyze_csv_files()
    print("分析完成")

if __name__ == "__main__":
    main()