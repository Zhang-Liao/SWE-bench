# SWE-bench 数据保存指南

本指南介绍如何将SWE-bench数据集保存到本地JSON文件中。

## 可用的脚本

### 1. `save_single_dataset.py` - 简单版本（推荐）
保存主要的SWE-bench数据集到JSON文件。

```bash
python save_single_dataset.py
```

**功能:**
- 保存 SWE-bench 主数据集的 test 和 dev 分割
- 保存 SWE-bench Lite 数据集的 test 和 dev 分割
- 自动创建 `swebench_data` 目录
- 显示数据集统计信息

### 2. `save_main_swebench.py` - 中等版本
保存更多数据集版本。

```bash
python save_main_swebench.py
```

**功能:**
- 保存 SWE-bench、SWE-bench Lite、SWE-bench Verified
- 包含数据集信息文件
- 生成总体统计

### 3. `save_swebench_to_json.py` - 完整版本
保存所有可用的SWE-bench数据集。

```bash
python save_swebench_to_json.py
```

**功能:**
- 保存所有SWE-bench数据集变体
- 包括多模态数据集
- 详细的统计信息

## 输出文件结构

运行脚本后，会在 `swebench_data/` 目录下生成以下文件：

```
swebench_data/
├── SWE-bench_test.json          # 主数据集测试集
├── SWE-bench_dev.json           # 主数据集开发集
├── SWE-bench_Lite_test.json     # Lite版本测试集
├── SWE-bench_Lite_dev.json      # Lite版本开发集
├── SWE-bench_Verified_test.json # 验证版本测试集
├── SWE-bench_Verified_dev.json  # 验证版本开发集
└── summary.json                 # 总体统计信息
```

## 数据集说明

### SWE-bench (主数据集)
- **来源**: `princeton-nlp/SWE-bench`
- **大小**: 约 2,294 个测试实例
- **描述**: 完整的SWE-bench数据集，包含来自GitHub的真实软件工程问题

### SWE-bench Lite
- **来源**: `SWE-bench/SWE-bench_Lite`
- **大小**: 约 300 个测试实例
- **描述**: 轻量级版本，用于快速测试和开发

### SWE-bench Verified
- **来源**: `SWE-bench/SWE-bench_Verified`
- **大小**: 约 500 个测试实例
- **描述**: 经过软件工程师验证的可解决问题子集

## 使用保存的数据

### 加载JSON数据
```python
import json

# 加载测试数据
with open('swebench_data/SWE-bench_test.json', 'r') as f:
    test_data = json.load(f)

print(f"加载了 {len(test_data)} 个测试实例")

# 查看第一个实例
first_instance = test_data[0]
print(f"实例ID: {first_instance['instance_id']}")
print(f"问题描述: {first_instance['problem_statement']}")
```

### 数据字段说明
每个实例包含以下主要字段：
- `instance_id`: 唯一标识符
- `problem_statement`: 问题描述
- `patch`: 解决方案补丁
- `test_patch`: 测试补丁
- `repo`: 仓库信息
- `base_commit`: 基础提交
- `patch`: 修复补丁

## 注意事项

1. **存储空间**: 完整数据集可能需要几GB的存储空间
2. **网络连接**: 首次下载需要稳定的网络连接
3. **内存使用**: 大型数据集可能需要较多内存
4. **文件编码**: 所有文件使用UTF-8编码保存

## 故障排除

### 网络连接问题
如果下载失败，可以重试：
```bash
python save_single_dataset.py
```

### 内存不足
如果遇到内存问题，可以分批处理：
```python
# 只保存特定数据集
from save_single_dataset import save_dataset_to_json
save_dataset_to_json("princeton-nlp/SWE-bench", "test", "my_test_data.json")
```

### 权限问题
确保有写入权限：
```bash
chmod +x save_single_dataset.py
python save_single_dataset.py
```

## 更多信息

- [SWE-bench 官方文档](https://swebench.github.io/)
- [Hugging Face 数据集页面](https://huggingface.co/datasets/princeton-nlp/SWE-bench)
- [GitHub 仓库](https://github.com/princeton-nlp/SWE-bench)

