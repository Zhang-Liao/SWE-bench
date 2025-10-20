from datasets import load_dataset
swebench = load_dataset('princeton-nlp/SWE-bench', split='test')

# 显示数据集基本信息
print("=== 数据集基本信息 ===")
print(f"数据集大小: {len(swebench)} 个测试用例")
print(f"数据集特征: {swebench.features}")
print(f"数据集列名: {swebench.column_names}")

# 显示第一个测试用例的详细信息
print("\n=== 第一个测试用例详情 ===")
first_instance = swebench[0]
for key, value in first_instance.items():
    if key == 'patch' or key == 'test_patch':
        print(f"{key}: {value[:200]}..." if len(str(value)) > 200 else f"{key}: {value}")
    else:
        print(f"{key}: {value}")

# 显示数据集统计信息
print("\n=== 数据集统计信息 ===")
print(f"包含测试套件的实例数量: {sum(1 for x in swebench if x.get('test_patch', '').strip())}")
print(f"包含补丁的实例数量: {sum(1 for x in swebench if x.get('patch', '').strip())}")

# 显示前几个实例的ID
print("\n=== 前10个测试实例ID ===")
for i in range(min(10, len(swebench))):
    print(f"{i+1}. {swebench[i]['instance_id']}")