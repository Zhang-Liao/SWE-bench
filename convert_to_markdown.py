#!/usr/bin/env python3
"""
将SWE-bench_dev.json中的每个问题保存为独立的markdown文件
"""

import json
import os
from pathlib import Path
from datetime import datetime

def sanitize_filename(filename):
    """清理文件名，移除不安全的字符"""
    # 移除或替换不安全的字符
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # 限制文件名长度
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename.strip()

def format_markdown_content(problem):
    """将问题数据格式化为markdown内容"""
    
    # 基本信息
    instance_id = problem.get('instance_id', 'Unknown')
    repo = problem.get('repo', 'Unknown')
    version = problem.get('version', 'Unknown')
    created_at = problem.get('created_at', 'Unknown')
    
    # 问题描述
    problem_statement = problem.get('problem_statement', '')
    
    # 补丁信息
    patch = problem.get('patch', '')
    test_patch = problem.get('test_patch', '')
    
    # 测试信息
    fail_to_pass = problem.get('FAIL_TO_PASS', '[]')
    pass_to_pass = problem.get('PASS_TO_PASS', '[]')
    
    # 提示信息
    hints_text = problem.get('hints_text', '')
    
    # 构建markdown内容
    content = f"""# {instance_id}

## 基本信息

- **实例ID**: {instance_id}
- **仓库**: {repo}
- **版本**: {version}
- **创建时间**: {created_at}
- **基础提交**: {problem.get('base_commit', 'Unknown')}
- **环境设置提交**: {problem.get('environment_setup_commit', 'Unknown')}

## 问题描述

{problem_statement}

## 解决方案补丁

```diff
{patch}
```

## 测试补丁

```diff
{test_patch}
```

## 测试信息

### 失败的测试 (FAIL_TO_PASS)
{fail_to_pass}

### 通过的测试 (PASS_TO_PASS)
{pass_to_pass}

## 提示信息

{hints_text}

---

*此文件由SWE-bench数据自动生成*
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return content

def save_problems_to_markdown():
    """将SWE-bench_dev.json中的问题保存为markdown文件"""
    
    # 输入和输出路径
    input_file = "swebench_data/SWE-bench_dev.json"
    output_dir = "swebench_dev_markdown"
    
    print("🚀 开始处理SWE-bench_dev.json数据...")
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return
    
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    print(f"📁 输出目录: {output_dir}")
    
    # 读取JSON数据
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        print(f"✅ 成功读取 {len(problems)} 个问题")
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return
    
    # 处理每个问题
    success_count = 0
    error_count = 0
    
    for i, problem in enumerate(problems):
        try:
            # 获取实例ID作为文件名
            instance_id = problem.get('instance_id', f'problem_{i}')
            
            # 清理文件名
            safe_filename = sanitize_filename(instance_id)
            filename = f"{safe_filename}.md"
            filepath = os.path.join(output_dir, filename)
            
            # 生成markdown内容
            content = format_markdown_content(problem)
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            success_count += 1
            
            # 显示进度
            if (i + 1) % 10 == 0 or i == len(problems) - 1:
                print(f"📝 已处理 {i + 1}/{len(problems)} 个问题")
                
        except Exception as e:
            print(f"❌ 处理问题 {i} 时出错: {e}")
            error_count += 1
            continue
    
    # 创建索引文件
    create_index_file(output_dir, problems)
    
    print(f"\n🎉 处理完成!")
    print(f"✅ 成功保存: {success_count} 个文件")
    print(f"❌ 失败: {error_count} 个文件")
    print(f"📁 输出目录: {os.path.abspath(output_dir)}")

def create_index_file(output_dir, problems):
    """创建索引文件"""
    index_content = f"""# SWE-bench Dev 问题索引

本目录包含SWE-bench开发集中的所有问题，每个问题保存为独立的markdown文件。

## 统计信息

- **总问题数**: {len(problems)}
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 问题列表

"""
    
    # 按仓库分组
    repos = {}
    for problem in problems:
        repo = problem.get('repo', 'Unknown')
        if repo not in repos:
            repos[repo] = []
        repos[repo].append(problem)
    
    # 生成索引内容
    for repo, repo_problems in sorted(repos.items()):
        index_content += f"\n### {repo} ({len(repo_problems)} 个问题)\n\n"
        
        for problem in sorted(repo_problems, key=lambda x: x.get('instance_id', '')):
            instance_id = problem.get('instance_id', 'Unknown')
            safe_filename = sanitize_filename(instance_id)
            filename = f"{safe_filename}.md"
            
            # 获取问题描述的第一行作为标题
            problem_statement = problem.get('problem_statement', '')
            title = problem_statement.split('\n')[0][:100] if problem_statement else 'No description'
            
            index_content += f"- [{instance_id}]({filename}) - {title}\n"
    
    # 保存索引文件
    index_path = os.path.join(output_dir, "README.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"📋 已创建索引文件: {index_path}")

def main():
    """主函数"""
    print("📄 SWE-bench Dev 问题转Markdown工具")
    print("=" * 50)
    
    save_problems_to_markdown()

if __name__ == "__main__":
    main()
