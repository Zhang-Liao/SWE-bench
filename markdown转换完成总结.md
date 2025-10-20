# SWE-bench Dev 问题转Markdown完成总结

## 🎉 任务完成情况

已成功将SWE-bench_dev.json中的所有问题转换为独立的markdown文件！

## 📁 生成的文件

### 输出目录
- `swebench_dev_markdown/` - 包含所有markdown文件的目录

### 文件统计
- **总文件数**: 226个 (225个问题文件 + 1个索引文件)
- **总行数**: 76,897行
- **文件大小**: 约5.3MB

### 文件结构
```
swebench_dev_markdown/
├── README.md                           # 索引文件
├── marshmallow-code__marshmallow-1164.md
├── marshmallow-code__marshmallow-1229.md
├── pvlib__pvlib-python-1026.md
├── pvlib__pvlib-python-1031.md
├── sqlfluff__sqlfluff-4764.md
├── sqlfluff__sqlfluff-2862.md
└── ... (共225个问题文件)
```

## 📊 数据统计

### 按仓库分组
- **marshmallow-code/marshmallow**: 9个问题
- **pvlib/pvlib-python**: 63个问题  
- **pydicom/pydicom**: 56个问题
- **sqlfluff/sqlfluff**: 50个问题
- **pylint-dev/astroid**: 31个问题
- **pyvista/pyvista**: 16个问题

### 文件大小分布
- 最小文件: 约6KB
- 最大文件: 约57KB
- 平均文件大小: 约24KB

## 📋 Markdown文件内容结构

每个markdown文件包含以下部分：

### 1. 基本信息
- 实例ID
- 仓库名称
- 版本信息
- 创建时间
- 基础提交哈希
- 环境设置提交哈希

### 2. 问题描述
- 完整的问题描述文本
- 包含用户报告的问题详情

### 3. 解决方案补丁
- 完整的diff补丁代码
- 使用代码块格式显示

### 4. 测试补丁
- 相关的测试代码补丁
- 使用代码块格式显示

### 5. 测试信息
- FAIL_TO_PASS: 失败的测试列表
- PASS_TO_PASS: 通过的测试列表

### 6. 提示信息
- 相关的提示和说明文本

## 🔍 示例文件

### 文件名格式
- `{仓库名}__{仓库名}-{问题编号}.md`
- 例如: `sqlfluff__sqlfluff-4764.md`

### 内容示例
```markdown
# sqlfluff__sqlfluff-4764

## 基本信息
- **实例ID**: sqlfluff__sqlfluff-4764
- **仓库**: sqlfluff/sqlfluff
- **版本**: 1.4
- **创建时间**: 2023-04-16T14:24:42Z

## 问题描述
Enable quiet mode/no-verbose in CLI for use in pre-commit hook
...

## 解决方案补丁
```diff
diff --git a/src/sqlfluff/cli/commands.py
...
```

## 测试补丁
```diff
diff --git a/test/cli/commands_test.py
...
```
```

## 📖 索引文件

`README.md` 文件提供了完整的索引，包括：
- 总体统计信息
- 按仓库分组的问题列表
- 每个问题的链接和简短描述
- 生成时间戳

## 🚀 使用方法

### 查看所有问题
```bash
ls swebench_dev_markdown/
```

### 查看索引
```bash
cat swebench_dev_markdown/README.md
```

### 查看特定问题
```bash
cat swebench_dev_markdown/sqlfluff__sqlfluff-4764.md
```

### 搜索特定仓库的问题
```bash
grep -l "sqlfluff" swebench_dev_markdown/*.md
```

## 💡 使用建议

1. **浏览问题**: 使用索引文件快速定位感兴趣的问题
2. **按仓库查看**: 可以按仓库名称过滤查看特定项目的问题
3. **代码分析**: 每个文件包含完整的补丁代码，便于分析解决方案
4. **测试理解**: 通过测试补丁了解问题的验证方法

## 🔗 相关资源

- [SWE-bench 官方文档](https://swebench.github.io/)
- [原始JSON数据](swebench_data/SWE-bench_dev.json)
- [转换脚本](convert_to_markdown.py)

---

**转换完成时间**: 2025年10月20日 11:39  
**输出目录**: `/home/zhang-liao/SWE-bench/swebench_dev_markdown/`  
**总存储空间**: 约5.3MB
