# sino-scrub 设计文档

**日期:** 2026-02-27
**版本:** 1.0
**状态:** 已批准

## 项目概述

`sino-scrub` 是一个 Python CLI 工具,用于毫秒级清洗 AI 生成文本中的中文文化敏感词和翻译错误。基于 FlashText 算法,比正则表达式快几十倍。

**核心价值:**
- 防止 AI 生成内容中的文化禁忌和翻译硬伤
- 毫秒级处理速度,不影响 API 响应时间
- 开箱即用的内置词库 + 灵活的自定义扩展

## 架构设计

### 目录结构

```
sino-scrub/
├── src/
│   └── sino_scrub/
│       ├── __init__.py          # 导出核心 API
│       ├── __main__.py          # CLI 入口点
│       ├── cli.py               # 命令行参数处理
│       ├── processor.py         # FlashText 封装
│       └── data/
│           └── default_dict.json  # 内置词库
├── tests/
│   └── test_processor.py        # 核心功能测试
├── pyproject.toml               # Poetry 配置
└── README.md
```

### 核心组件

**1. processor.py - 文本清洗引擎**
- 封装 FlashText 的 `KeywordProcessor`
- 加载内置词库 + 可选的用户词库
- 提供 `scrub(text)` 方法返回清洗后的文本

**2. cli.py - 命令行接口**
- 使用 Typer 构建 CLI
- 支持参数: `scrub "文本"` 或 `scrub file.txt`
- 支持选项: `--custom-dict`, `--diff`

**3. default_dict.json - 内置词库**
- 简单的 JSON 键值对格式
- 包含 20-30 个高频敏感词

## 核心 API

### TextScrubber 类

```python
from flashtext import KeywordProcessor
import json
from pathlib import Path

class TextScrubber:
    def __init__(self, custom_dict_path=None):
        self.processor = KeywordProcessor()
        self._load_builtin_dict()
        if custom_dict_path:
            self._load_custom_dict(custom_dict_path)

    def scrub(self, text: str) -> str:
        """清洗文本,返回替换后的结果"""
        return self.processor.replace_keywords(text)
```

### CLI 使用方式

```bash
# 基本用法
scrub "系统正在处死进程"              # 直接清洗文本
scrub file.txt                        # 清洗文件内容
scrub file.txt --custom-dict my.json  # 使用自定义词库
scrub "文本" --diff                   # 显示对比
```

### 作为 Python 库使用

```python
from sino_scrub import TextScrubber

scrubber = TextScrubber()
clean_text = scrubber.scrub("系统正在处死进程")
```

## 数据流

```
用户输入
    ↓
CLI 解析参数
    ↓
TextScrubber 初始化
    ├─ 加载 default_dict.json (内置)
    └─ 加载 custom_dict.json (可选)
    ↓
FlashText 替换关键词
    ↓
输出清洗后的文本
```

## 错误处理

| 场景 | 行为 | 退出码 |
|------|------|--------|
| 内置词库加载失败 | `[ERROR]` 退出 | 1 |
| 自定义词库不存在 | `[WARN]` 继续运行 | 0 |
| 自定义词库格式错误 | `[ERROR]` 退出 | 1 |
| 输入文件不存在 | `[ERROR]` 退出 | 1 |
| 输入文件读取失败 | `[ERROR]` 退出 | 1 |

### 词库合并策略

- 先加载内置词库
- 再加载自定义词库
- 如果有重复的 key,自定义词库优先级更高(覆盖内置规则)

## 内置词库设计

### default_dict.json 内容规划

包含 3 大类高频敏感词(20-30 个):

**1. 翻译修正类** (10 个)
```json
{
  "处死": "终止",
  "执行程序": "运行程序",
  "杀死进程": "终止进程",
  "致命错误": "严重错误"
}
```

**2. 文化禁忌类** (10 个)
```json
{
  "升天": "幸福",
  "绿帽子": "精美帽子",
  "送钟": "送礼物",
  "白色信封": "红色信封"
}
```

**3. 敏感称谓类** (5-10 个)
```json
{
  "台湾国": "台湾地区",
  "中国台湾": "中国台湾地区"
}
```

### 词库维护原则

- 只收录**高频、明显**的错误
- 避免过度审查(不做语义分析)
- 用户可通过自定义词库扩展

## 技术栈

### 核心依赖

- `flashtext` - 关键词替换引擎
- `typer` - CLI 框架
- `rich` - 终端输出美化(仅用于 `--diff` 模式)

### 开发依赖

- `pytest` - 测试框架
- `poetry` - 包管理

## 测试策略

### 核心测试用例

1. 基本替换功能 - 验证单个词替换
2. 多词替换 - 验证一次性替换多个敏感词
3. 自定义词库优先级 - 验证用户词库覆盖内置词库
4. 无匹配情况 - 验证原文不变
5. 错误处理 - 验证词库加载失败的降级行为

### 不测试的内容

- FlashText 库本身的正确性(已有上游测试)
- 终端颜色渲染效果

## 性能目标

- 加载 1000 个词条的词库: < 100ms
- 处理 10KB 文本: < 10ms
- 满足"毫秒级"承诺

## 设计决策

### 为什么选择极简 MVP?

1. **快速验证核心价值** - 先验证 FlashText 速度优势
2. **符合用户选择** - 简单 JSON 格式,友好错误处理
3. **YAGNI 原则** - 分类词库和 Debug Mode 可后续迭代

### 为什么 CLI 优先?

- 开发者和运营人员的主要使用场景
- 可以直接在终端查看清洗效果
- 同时支持作为库导入,满足集成需求

### 为什么使用 FlashText?

- O(N) 复杂度,比正则表达式快几十倍
- 适合海量关键词场景
- 简单易用,无需复杂配置

## 后续迭代方向

1. **分类词库** - 支持按类别加载词库
2. **Debug Mode** - 显示替换原因,增强传播性
3. **词库管理工具** - CLI 命令管理词库
4. **性能优化** - 词库预编译和缓存
