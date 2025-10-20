#!/usr/bin/env python3
"""
SWE-bench数据使用示例
展示如何加载和使用保存的JSON数据
"""

import json
import os
from pathlib import Path

def load_swebench_data(data_file):
    """加载SWE-bench数据"""
    print(f"📂 加载数据文件: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ 成功加载 {len(data)} 条记录")
    return data

def analyze_data(data, dataset_name):
    """分析数据集"""
    print(f"\n📊 {dataset_name} 数据分析:")
    print(f"   总记录数: {len(data)}")
    
    # 统计仓库分布
    repos = {}
    for item in data:
        repo = item.get('repo', 'unknown')
        repos[repo] = repos.get(repo, 0) + 1
    
    print(f"   涉及仓库数: {len(repos)}")
    print(f"   主要仓库:")
    for repo, count in sorted(repos.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"     - {repo}: {count} 个问题")
    
    # 统计有补丁的记录
    with_patch = sum(1 for item in data if item.get('patch', '').strip())
    with_test = sum(1 for item in data if item.get('test_patch', '').strip())
    
    print(f"   包含补丁的记录: {with_patch} ({with_patch/len(data)*100:.1f}%)")
    print(f"   包含测试的记录: {with_test} ({with_test/len(data)*100:.1f}%)")
    
    return repos

def show_sample_problem(data, index=0):
    """显示示例问题"""
    if index >= len(data):
        print(f"❌ 索引 {index} 超出范围")
        return
    
    item = data[index]
    print(f"\n🔍 示例问题 #{index + 1}:")
    print(f"   实例ID: {item.get('instance_id', 'N/A')}")
    print(f"   仓库: {item.get('repo', 'N/A')}")
    print(f"   版本: {item.get('version', 'N/A')}")
    print(f"   创建时间: {item.get('created_at', 'N/A')}")
    
    # 问题描述（截取前500字符）
    problem = item.get('problem_statement', '')
    if len(problem) > 500:
        problem = problem[:500] + "..."
    print(f"   问题描述: {problem}")
    
    # 补丁信息
    patch = item.get('patch', '')
    if patch:
        print(f"   补丁长度: {len(patch)} 字符")
        print(f"   补丁预览: {patch[:200]}...")
    
    # 测试信息
    test_patch = item.get('test_patch', '')
    if test_patch:
        print(f"   测试补丁长度: {len(test_patch)} 字符")
    
    # 失败的测试
    fail_tests = item.get('FAIL_TO_PASS', [])
    if fail_tests:
        print(f"   失败的测试: {fail_tests}")

def search_by_repo(data, repo_name):
    """按仓库搜索问题"""
    matching_items = [item for item in data if item.get('repo', '').lower() == repo_name.lower()]
    
    print(f"\n🔍 在 {repo_name} 仓库中找到 {len(matching_items)} 个问题:")
    
    for i, item in enumerate(matching_items[:5]):  # 只显示前5个
        print(f"   {i+1}. {item.get('instance_id', 'N/A')} - {item.get('problem_statement', '')[:100]}...")
    
    if len(matching_items) > 5:
        print(f"   ... 还有 {len(matching_items) - 5} 个问题")

def main():
    """主函数"""
    print("🚀 SWE-bench数据使用示例")
    print("=" * 60)
    
    data_dir = "swebench_data"
    
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录不存在: {data_dir}")
        print("请先运行 save_single_dataset.py 下载数据")
        return
    
    # 加载主要数据集
    test_file = os.path.join(data_dir, "SWE-bench_test.json")
    dev_file = os.path.join(data_dir, "SWE-bench_dev.json")
    lite_file = os.path.join(data_dir, "SWE-bench_Lite_test.json")
    
    datasets = {}
    
    if os.path.exists(test_file):
        datasets["SWE-bench Test"] = load_swebench_data(test_file)
    
    if os.path.exists(dev_file):
        datasets["SWE-bench Dev"] = load_swebench_data(dev_file)
    
    if os.path.exists(lite_file):
        datasets["SWE-bench Lite"] = load_swebench_data(lite_file)
    
    if not datasets:
        print("❌ 没有找到数据文件")
        return
    
    # 分析每个数据集
    all_repos = {}
    for name, data in datasets.items():
        repos = analyze_data(data, name)
        all_repos.update(repos)
    
    # 显示总体统计
    print(f"\n📈 总体统计:")
    print(f"   数据集数量: {len(datasets)}")
    print(f"   总记录数: {sum(len(data) for data in datasets.values())}")
    print(f"   涉及仓库总数: {len(all_repos)}")
    
    # 显示示例问题
    if "SWE-bench Test" in datasets:
        show_sample_problem(datasets["SWE-bench Test"], 0)
    
    # 搜索特定仓库
    if "SWE-bench Test" in datasets:
        print(f"\n🔍 搜索示例:")
        search_by_repo(datasets["SWE-bench Test"], "astropy/astropy")
    
    print(f"\n💡 使用提示:")
    print(f"   - 所有数据都保存在 {os.path.abspath(data_dir)} 目录中")
    print(f"   - 可以使用标准JSON库加载数据")
    print(f"   - 每个记录包含完整的问题描述、补丁和测试信息")

if __name__ == "__main__":
    main()

