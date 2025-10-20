#!/usr/bin/env python3
"""
SWE-bench数据集保存脚本
将SWE-bench的所有数据集保存到JSON文件中
"""

import json
import os
from datasets import load_dataset
from pathlib import Path
from typing import Dict, Any, List

def save_dataset_to_json(dataset, filename: str, output_dir: str = "swebench_data") -> None:
    """
    将数据集保存为JSON文件
    
    Args:
        dataset: Hugging Face数据集对象
        filename: 输出文件名
        output_dir: 输出目录
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    # 将数据集转换为列表
    data_list = [item for item in dataset]
    
    # 保存为JSON文件
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已保存 {len(data_list)} 条记录到 {output_path}")

def save_dataset_info(dataset, filename: str, output_dir: str = "swebench_data") -> None:
    """
    保存数据集信息到JSON文件
    
    Args:
        dataset: Hugging Face数据集对象
        filename: 输出文件名
        output_dir: 输出目录
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    # 收集数据集信息
    info = {
        "size": len(dataset),
        "features": str(dataset.features),
        "column_names": dataset.column_names,
        "split": getattr(dataset, 'split', 'unknown'),
        "description": getattr(dataset, 'description', ''),
    }
    
    # 保存信息文件
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已保存数据集信息到 {output_path}")

def main():
    """主函数"""
    print("🚀 开始下载和保存SWE-bench数据集...")
    
    # 定义要下载的数据集
    datasets_to_download = {
        "SWE-bench": {
            "name": "princeton-nlp/SWE-bench",
            "splits": ["test", "dev"]
        },
        "SWE-bench_Lite": {
            "name": "SWE-bench/SWE-bench_Lite", 
            "splits": ["test", "dev"]
        },
        "SWE-bench_Verified": {
            "name": "SWE-bench/SWE-bench_Verified",
            "splits": ["test", "dev"]
        },
        "SWE-bench_Multimodal": {
            "name": "SWE-bench/SWE-bench_Multimodal",
            "splits": ["test", "dev"]
        }
    }
    
    # 创建主输出目录
    main_output_dir = "swebench_data"
    Path(main_output_dir).mkdir(exist_ok=True)
    
    # 下载和保存每个数据集
    for dataset_name, config in datasets_to_download.items():
        print(f"\n📦 正在处理 {dataset_name}...")
        
        try:
            # 加载数据集
            dataset = load_dataset(config["name"])
            
            # 为每个split保存数据
            for split in config["splits"]:
                if split in dataset:
                    print(f"  📁 保存 {split} 分割...")
                    
                    # 保存数据
                    data_filename = f"{dataset_name}_{split}.json"
                    save_dataset_to_json(dataset[split], data_filename, main_output_dir)
                    
                    # 保存信息
                    info_filename = f"{dataset_name}_{split}_info.json"
                    save_dataset_info(dataset[split], info_filename, main_output_dir)
                else:
                    print(f"  ⚠️  {split} 分割不存在于 {dataset_name}")
                    
        except Exception as e:
            print(f"  ❌ 下载 {dataset_name} 时出错: {str(e)}")
            continue
    
    # 创建总体统计文件
    print(f"\n📊 创建总体统计文件...")
    create_summary_stats(main_output_dir)
    
    print(f"\n🎉 所有数据集已保存到 {main_output_dir} 目录！")
    print(f"📁 目录结构:")
    print(f"   {main_output_dir}/")
    print(f"   ├── SWE-bench_test.json")
    print(f"   ├── SWE-bench_test_info.json")
    print(f"   ├── SWE-bench_dev.json")
    print(f"   ├── SWE-bench_dev_info.json")
    print(f"   ├── SWE-bench_Lite_test.json")
    print(f"   ├── SWE-bench_Lite_test_info.json")
    print(f"   ├── ...")
    print(f"   └── summary_stats.json")

def create_summary_stats(output_dir: str) -> None:
    """创建总体统计文件"""
    stats = {
        "total_datasets": 0,
        "total_instances": 0,
        "datasets": {}
    }
    
    # 扫描输出目录中的所有JSON文件
    for file_path in Path(output_dir).glob("*.json"):
        if file_path.name.endswith("_info.json"):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            dataset_name = file_path.stem
            stats["datasets"][dataset_name] = {
                "file_path": str(file_path),
                "instance_count": len(data),
                "file_size_mb": round(file_path.stat().st_size / (1024 * 1024), 2)
            }
            stats["total_instances"] += len(data)
            stats["total_datasets"] += 1
            
        except Exception as e:
            print(f"  ⚠️ 处理 {file_path} 时出错: {str(e)}")
    
    # 保存统计信息
    stats_path = os.path.join(output_dir, "summary_stats.json")
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已保存统计信息到 {stats_path}")
    print(f"📈 总计: {stats['total_datasets']} 个数据集, {stats['total_instances']} 个实例")

if __name__ == "__main__":
    main()

