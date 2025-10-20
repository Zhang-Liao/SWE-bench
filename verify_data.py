#!/usr/bin/env python3
"""
验证保存的SWE-bench数据
"""

import json
import os
from pathlib import Path

def verify_json_file(filepath):
    """验证JSON文件"""
    print(f"🔍 验证文件: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ 文件有效，包含 {len(data)} 条记录")
        
        # 显示第一条记录的关键信息
        if data:
            first_record = data[0]
            print(f"   第一条记录ID: {first_record.get('instance_id', 'N/A')}")
            print(f"   仓库: {first_record.get('repo', 'N/A')}")
            print(f"   问题描述长度: {len(first_record.get('problem_statement', ''))}")
            print(f"   补丁长度: {len(first_record.get('patch', ''))}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔍 验证SWE-bench数据文件")
    print("=" * 50)
    
    data_dir = "swebench_data"
    
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录不存在: {data_dir}")
        return
    
    # 获取所有JSON文件
    json_files = list(Path(data_dir).glob("*.json"))
    
    if not json_files:
        print(f"❌ 在 {data_dir} 中没有找到JSON文件")
        return
    
    print(f"📁 找到 {len(json_files)} 个JSON文件")
    print()
    
    # 验证每个文件
    valid_files = 0
    total_records = 0
    
    for file_path in sorted(json_files):
        if verify_json_file(str(file_path)):
            valid_files += 1
            
            # 计算记录数
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                total_records += len(data)
            except:
                pass
        
        print()
    
    print("=" * 50)
    print(f"📊 验证结果:")
    print(f"   有效文件: {valid_files}/{len(json_files)}")
    print(f"   总记录数: {total_records}")
    print(f"   数据目录: {os.path.abspath(data_dir)}")
    
    if valid_files == len(json_files):
        print("🎉 所有文件验证通过！")
    else:
        print("⚠️ 部分文件验证失败")

if __name__ == "__main__":
    main()

