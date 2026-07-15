# Contributing to LovTrip

感谢你对 LovTrip 的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 🐛 报告 Bug

1. 使用 GitHub Issues 提交 bug
2. 描述复现步骤
3. 提供期望行为 vs 实际行为
4. 附上截图（如有）
5. 说明运行环境（OS、Python 版本等）

### 💡 功能建议

1. 在 Issues 中使用 "Feature Request" 标签
2. 描述你希望添加的功能
3. 说明使用场景和价值

### 🔧 提交代码

1. Fork 本仓库
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 确保代码通过测试: `pytest tests/`
4. 确保代码风格: `ruff check . && black .`
5. 提交变更: `git commit -m 'feat: add amazing feature'`
6. 推送分支: `git push origin feature/amazing-feature`
7. 创建 Pull Request

### Commit 规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具

### 开发环境设置

```bash
git clone https://github.com/ziqingzhou68-hue/lovtrip.git
cd lovtrip
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
# 编辑 .env 填入 API Key
streamlit run streamlit_app.py
```

### 代码风格

- 遵循 PEP 8
- 使用 `black` 格式化代码
- 使用 `ruff` 进行 lint
- 为新功能编写测试
- 保持函数简短、职责单一

## 分支策略

- `main` — 生产就绪代码
- `develop` — 开发分支
- `feature/*` — 功能分支
- `fix/*` — 修复分支

## 问题与帮助

如有任何问题，欢迎在 GitHub Issues 中提问或联系维护者。
