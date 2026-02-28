# Contributing to sino-scrub / 贡献指南

## English

Thank you for your interest in contributing to sino-scrub! This document provides guidelines for contributing to this project.

### Project Status

This is currently a personal project maintained by [PerryLink](https://github.com/PerryLink). While contributions are welcome, please note that this is an individual effort and response times may vary.

### How to Report Issues

If you encounter a bug or have a feature request:

1. Check the [existing issues](https://github.com/PerryLink/sino-scrub/issues) to avoid duplicates
2. Create a new issue with a clear title and description
3. For bugs, include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Python version and OS
   - Relevant code snippets or error messages

### Development Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PerryLink/sino-scrub.git
   cd sino-scrub
   ```

2. **Install dependencies**:

   Using Poetry (recommended):
   ```bash
   poetry install
   ```

   Or using pip:
   ```bash
   pip install -e .
   pip install pytest pytest-cov black ruff
   ```

3. **Run tests**:
   ```bash
   poetry run pytest
   # or
   pytest
   ```

4. **Run the CLI**:
   ```bash
   poetry run scrub "测试文本"
   # or
   python -m sino_scrub "测试文本"
   ```

### Code Standards

- **Style Guide**: Follow [PEP 8](https://pep8.org/) Python style guide
- **Formatting**: Use `black` for code formatting
  ```bash
  black src/ tests/
  ```
- **Linting**: Use `ruff` for linting
  ```bash
  ruff check src/ tests/
  ```
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: Use docstrings for public functions and classes
- **Testing**: Write tests for new features and bug fixes

### Pull Request Process

1. **Fork the repository** and create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, readable code
   - Add tests for new functionality
   - Update documentation if needed

3. **Run tests and linting**:
   ```bash
   pytest
   black src/ tests/
   ruff check src/ tests/
   ```

4. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Follow the format: `type: description`
   - Examples: `feat: add custom dictionary support`, `fix: handle empty input`

5. **Push to your fork** and create a pull request:
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all tests pass

6. **Wait for review**:
   - The maintainer will review your PR
   - Address any feedback or requested changes
   - Once approved, your PR will be merged

### Code of Conduct

- Be respectful and constructive
- Focus on the code, not the person
- Accept constructive criticism gracefully
- Help create a welcoming environment for all contributors

---

## 中文

感谢您对 sino-scrub 项目的关注！本文档提供了贡献指南。

### 项目状态

这是一个由 [PerryLink](https://github.com/PerryLink) 个人维护的项目。欢迎贡献，但请注意这是个人项目，响应时间可能会有所不同。

### 如何报告问题

如果您遇到 bug 或有功能建议：

1. 检查[现有 issues](https://github.com/PerryLink/sino-scrub/issues) 避免重复
2. 创建新 issue，提供清晰的标题和描述
3. 对于 bug，请包含：
   - 复现步骤
   - 期望行为
   - 实际行为
   - Python 版本和操作系统
   - 相关代码片段或错误信息

### 开发环境搭建

1. **克隆仓库**：
   ```bash
   git clone https://github.com/PerryLink/sino-scrub.git
   cd sino-scrub
   ```

2. **安装依赖**：

   使用 Poetry（推荐）：
   ```bash
   poetry install
   ```

   或使用 pip：
   ```bash
   pip install -e .
   pip install pytest pytest-cov black ruff
   ```

3. **运行测试**：
   ```bash
   poetry run pytest
   # 或
   pytest
   ```

4. **运行 CLI**：
   ```bash
   poetry run scrub "测试文本"
   # 或
   python -m sino_scrub "测试文本"
   ```

### 代码规范

- **风格指南**：遵循 [PEP 8](https://pep8.org/) Python 代码风格
- **格式化**：使用 `black` 格式化代码
  ```bash
  black src/ tests/
  ```
- **代码检查**：使用 `ruff` 进行代码检查
  ```bash
  ruff check src/ tests/
  ```
- **类型提示**：适当使用类型提示
- **文档字符串**：为公共函数和类添加文档字符串
- **测试**：为新功能和 bug 修复编写测试

### Pull Request 流程

1. **Fork 仓库**并创建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **进行修改**：
   - 编写清晰、可读的代码
   - 为新功能添加测试
   - 必要时更新文档

3. **运行测试和代码检查**：
   ```bash
   pytest
   black src/ tests/
   ruff check src/ tests/
   ```

4. **提交更改**：
   - 使用清晰、描述性的提交信息
   - 遵循格式：`type: description`
   - 示例：`feat: 添加自定义词库支持`、`fix: 处理空输入`

5. **推送到您的 fork** 并创建 pull request：
   - 提供清晰的更改描述
   - 引用相关 issues
   - 确保所有测试通过

6. **等待审查**：
   - 维护者会审查您的 PR
   - 根据反馈进行修改
   - 批准后，您的 PR 将被合并

### 行为准则

- 保持尊重和建设性
- 关注代码，而非个人
- 优雅地接受建设性批评
- 帮助创建一个欢迎所有贡献者的环境

---

## Contact / 联系方式

- **Email / 邮箱**: novelnexusai@outlook.com
- **GitHub**: [@PerryLink](https://github.com/PerryLink)

Thank you for contributing! / 感谢您的贡献！
