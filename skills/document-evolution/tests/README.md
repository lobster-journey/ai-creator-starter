# 文档阅读与进化 - 测试用例

## 测试环境

```bash
# 安装依赖
pip install pytest
pip install pylint

# 进入测试目录
cd ~/.openclaw/skills/document-evolution
```

---

## 单元测试

### 测试1：文档管理器初始化

```python
# test_evolve.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.evolve import DocumentEvolution

def test_init():
    """测试管理器初始化"""
    manager = DocumentEvolution()
    assert manager.workspace is not None
    assert manager.output_dir is not None
    print("✅ 管理器初始化测试通过")

if __name__ == '__main__':
    test_init()
```

### 测试2：报告生成

```python
def test_generate_report():
    """测试报告生成"""
    manager = DocumentEvolution()
    
    summary = "文档总结内容"
    business = "业务分析内容"
    technical = "技术分析内容"
    
    report_file = manager.generate_report(
        "https://example.com",
        summary,
        business,
        technical
    )
    
    assert os.path.exists(report_file)
    print("✅ 报告生成测试通过")
```

---

## 集成测试

### 测试3：完整流程

```bash
#!/bin/bash
# test_full_workflow.sh

echo "=== 测试完整流程 ==="

# 1. 创建测试文档
TEST_DOC="/tmp/test_doc.md"
cat > $TEST_DOC << EOF
# 测试文档

这是测试文档内容。
EOF

# 2. 运行脚本
python3 ~/.openclaw/skills/document-evolution/scripts/evolve.py \
  "https://example.com/test" \
  --type web

# 3. 检查输出
OUTPUT_DIR="$HOME/.openclaw/workspace/document_evolution"
if [ -d "$OUTPUT_DIR" ]; then
    echo "✅ 输出目录创建成功"
else
    echo "❌ 输出目录创建失败"
    exit 1
fi

# 4. 检查报告文件
REPORT_COUNT=$(ls -1 $OUTPUT_DIR/report_*.md 2>/dev/null | wc -l)
if [ $REPORT_COUNT -gt 0 ]; then
    echo "✅ 报告文件生成成功"
else
    echo "❌ 报告文件生成失败"
    exit 1
fi

echo "=== 测试完成 ==="
```

---

## 运行测试

### 运行所有测试

```bash
# 单元测试
python3 test_evolve.py

# 集成测试
bash test_full_workflow.sh
```

### 使用pytest

```bash
# 安装pytest
pip install pytest

# 运行测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_evolve.py::test_init -v
```

---

## 代码质量检查

### Pylint检查

```bash
# 安装pylint
pip install pylint

# 检查代码
pylint scripts/evolve.py --rcfile=.pylintrc
```

### 代码格式化

```bash
# 安装black
pip install black

# 格式化代码
black scripts/evolve.py
```

---

## 测试覆盖率

```bash
# 安装coverage
pip install coverage

# 运行测试并生成覆盖率报告
coverage run -m pytest tests/
coverage report
coverage html
```

---

## 注意事项

### 测试原则
- ✅ 每个功能都要有测试
- ✅ 测试用例要清晰
- ✅ 测试要独立运行
- ✅ 测试结果要明确

### 代码修改流程
1. 编写测试用例
2. 运行测试（应该失败）
3. 修改代码
4. 运行测试（应该通过）
5. 提交代码

---

*Created by 🦞 Lobster Journey Studio*
