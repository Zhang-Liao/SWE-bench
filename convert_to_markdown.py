#!/usr/bin/env python3
"""
将 SWE-bench_dev.json 和 SWE-bench_test.json 中的每个问题保存为独立的 markdown 文件。
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

# 数据集配置: (输入文件, 输出目录, 显示名称)
DATASET_CONFIG = {
    "dev": ("swebench_data/SWE-bench_dev.json", "swebench_dev_markdown", "Dev"),
    "test": ("swebench_data/SWE-bench_test.json", "swebench_test_markdown", "Test"),
}

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

def save_problems_to_markdown(input_file: str, output_dir: str, dataset_name: str):
    """将指定 JSON 中的问题保存为 markdown 文件。"""

    print(f"🚀 开始处理 {os.path.basename(input_file)} 数据...")

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return False

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
        return False

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
            if (i + 1) % 100 == 0 or i == len(problems) - 1:
                print(f"📝 已处理 {i + 1}/{len(problems)} 个问题")

        except Exception as e:
            print(f"❌ 处理问题 {i} 时出错: {e}")
            error_count += 1
            continue

    # 创建索引文件
    create_index_file(output_dir, problems, dataset_name)

    print(f"\n🎉 {dataset_name} 集处理完成!")
    print(f"✅ 成功保存: {success_count} 个文件")
    print(f"❌ 失败: {error_count} 个文件")
    print(f"📁 输出目录: {os.path.abspath(output_dir)}")
    return True

def create_index_file(output_dir, problems, dataset_name: str = "Dev"):
    """创建索引文件"""
    index_content = f"""# SWE-bench {dataset_name} 问题索引

本目录包含 SWE-bench {dataset_name} 集中的所有问题，每个问题保存为独立的 markdown 文件。

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
    parser = argparse.ArgumentParser(
        description="将 SWE-bench JSON 数据集转为 Markdown 文件"
    )
    parser.add_argument(
        "--dataset",
        choices=["dev", "test", "all"],
        default="all",
        help="要转换的数据集: dev=仅Dev集, test=仅Test集, all=两者 (默认: all)",
    )
    args = parser.parse_args()

    print("📄 SWE-bench 问题转 Markdown 工具")
    print("=" * 50)

    if args.dataset == "all":
        datasets = ["dev", "test"]
    else:
        datasets = [args.dataset]

    for name in datasets:
        input_file, output_dir, display_name = DATASET_CONFIG[name]
        save_problems_to_markdown(input_file, output_dir, display_name)
        if len(datasets) > 1:
            print()


if __name__ == "__main__":
    main()





