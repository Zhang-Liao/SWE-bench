#!/usr/bin/env python3
"""
保存单个SWE-bench数据集到JSON文件
使用方法: python save_single_dataset.py
"""

from datasets import load_dataset
import json
import os
from pathlib import Path

def save_dataset_to_json(dataset_name="princeton-nlp/SWE-bench", split="test", output_file=None):
    """
    保存指定数据集到JSON文件
    
    Args:
        dataset_name: 数据集名称
        split: 数据集分割 (test/dev)
        output_file: 输出文件名，如果为None则自动生成
    """
    print(f"🔄 正在加载数据集: {dataset_name} ({split})")
    
    try:
        # 加载数据集
        dataset = load_dataset(dataset_name)
        
        if split not in dataset:
            print(f"❌ 错误: 数据集 {dataset_name} 没有 {split} 分割")
            print(f"可用的分割: {list(dataset.keys())}")
            return
        
        # 获取指定分割的数据
        data = dataset[split]
        print(f"✅ 成功加载 {len(data)} 条记录")
        
        # 转换为列表
        data_list = [item for item in data]
        
        # 生成输出文件名
        if output_file is None:
            dataset_short = dataset_name.split('/')[-1]
            output_file = f"{dataset_short}_{split}.json"
        
        # 创建输出目录
        output_dir = "swebench_data"
        Path(output_dir).mkdir(exist_ok=True)
        
        # 保存到JSON文件
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 数据已保存到: {output_path}")
        print(f"📊 文件大小: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        
        # 显示数据集信息
        print(f"\n📋 数据集信息:")
        print(f"   大小: {len(data_list)} 条记录")
        print(f"   特征: {data.features}")
        print(f"   列名: {data.column_names}")
        
        # 显示第一个实例的键
        if data_list:
            print(f"\n🔍 第一个实例的字段:")
            for key in data_list[0].keys():
                value = data_list[0][key]
                if isinstance(value, str) and len(value) > 100:
                    print(f"   {key}: {value[:100]}...")
                else:
                    print(f"   {key}: {value}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return None

def main():
    """主函数 - 保存主要的SWE-bench数据集"""
    print("🚀 SWE-bench数据集保存工具")
    print("=" * 50)
    
    # 保存主要的SWE-bench数据集
    datasets_to_save = [
        ("princeton-nlp/SWE-bench", "test"),
        ("princeton-nlp/SWE-bench", "dev"),
        ("SWE-bench/SWE-bench_Lite", "test"),
        ("SWE-bench/SWE-bench_Lite", "dev")
    ]
    
    saved_files = []
    
    for dataset_name, split in datasets_to_save:
        print(f"\n{'='*50}")
        output_file = save_dataset_to_json(dataset_name, split)
        if output_file:
            saved_files.append(output_file)
    
    print(f"\n🎉 完成！")
    print(f"📁 保存的文件:")
    for file in saved_files:
        print(f"   - {file}")
    
    print(f"\n💡 提示: 所有文件都保存在 'swebench_data' 目录中")

if __name__ == "__main__":
    main()

