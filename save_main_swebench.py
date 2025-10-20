#!/usr/bin/env python3
"""
简化版SWE-bench数据集保存脚本
只保存主要的SWE-bench数据集到JSON文件
"""

import json
import os
from datasets import load_dataset
from pathlib import Path

def save_swebench_data():
    """保存SWE-bench主要数据集"""
    print("🚀 开始下载和保存SWE-bench数据集...")
    
    # 创建输出目录
    output_dir = "swebench_data"
    Path(output_dir).mkdir(exist_ok=True)
    
    # 要下载的数据集列表
    datasets = [
        ("princeton-nlp/SWE-bench", "SWE-bench"),
        ("SWE-bench/SWE-bench_Lite", "SWE-bench_Lite"),
        ("SWE-bench/SWE-bench_Verified", "SWE-bench_Verified")
    ]
    
    total_instances = 0
    
    for dataset_name, file_prefix in datasets:
        print(f"\n📦 正在处理 {file_prefix}...")
        
        try:
            # 加载数据集
            dataset = load_dataset(dataset_name)
            
            # 保存每个分割
            for split_name in ["test", "dev"]:
                if split_name in dataset:
                    print(f"  📁 保存 {split_name} 分割...")
                    
                    # 转换为列表
                    data_list = [item for item in dataset[split_name]]
                    
                    # 保存为JSON
                    filename = f"{file_prefix}_{split_name}.json"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data_list, f, indent=2, ensure_ascii=False)
                    
                    print(f"    ✅ 已保存 {len(data_list)} 条记录到 {filename}")
                    total_instances += len(data_list)
                    
                    # 保存数据集信息
                    info = {
                        "dataset_name": dataset_name,
                        "split": split_name,
                        "size": len(data_list),
                        "features": str(dataset[split_name].features),
                        "column_names": dataset[split_name].column_names
                    }
                    
                    info_filename = f"{file_prefix}_{split_name}_info.json"
                    info_filepath = os.path.join(output_dir, info_filename)
                    
                    with open(info_filepath, 'w', encoding='utf-8') as f:
                        json.dump(info, f, indent=2, ensure_ascii=False)
                    
                    print(f"    ✅ 已保存数据集信息到 {info_filename}")
                else:
                    print(f"  ⚠️  {split_name} 分割不存在")
                    
        except Exception as e:
            print(f"  ❌ 下载 {file_prefix} 时出错: {str(e)}")
            continue
    
    # 创建总体统计
    print(f"\n📊 创建总体统计...")
    stats = {
        "total_instances": total_instances,
        "output_directory": output_dir,
        "files_created": len(list(Path(output_dir).glob("*.json")))
    }
    
    stats_path = os.path.join(output_dir, "summary.json")
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 完成！")
    print(f"📁 数据保存在: {output_dir}/")
    print(f"📈 总计: {total_instances} 个实例")
    print(f"📄 文件数: {stats['files_created']} 个JSON文件")

if __name__ == "__main__":
    save_swebench_data()

