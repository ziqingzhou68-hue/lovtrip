# LovTrip 开发指南

> Development Guide

---

## 环境准备

### 系统要求

- Python 3.9+
- pip（Python 包管理）
- Git

### 本地开发环境

```bash
# 1. Clone 仓库
git clone https://github.com/ziqingzhou68-hue/lovtrip.git
cd lovtrip

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 配置 API Key
cp .env.example .env
# 编辑 .env，填入真实 API Key

# 5. 启动开发服务器
streamlit run streamlit_app.py
```

---

## 项目模块说明

### `config/` — 配置管理

```python
from config import (
    API_KEY,       # LLM API Key
    BASE_URL,      # LLM API Base URL
    MODEL,         # 模型名称
    BAIDU_AK,      # 百度地图 AK
    PEXELS_KEY,    # Pexels API Key
    SYSTEM_PROMPT, # LLM System Prompt
    get_config,    # 通用配置读取函数
)
```

### `services/baidu_map.py` — 百度地图服务

```python
from services.baidu_map import baidu_geocode, baidu_place_search

# 地理编码：城市名 → 经纬度
coords = baidu_geocode("北京")
# → {"lng": 116.404, "lat": 39.915}

# 地点搜索
spots = baidu_place_search("景点", coords["lng"], coords["lat"])
# → [{"name": "故宫", "address": "...", "location": {...}}, ...]
```

### `services/weather.py` — 天气服务

```python
from services.weather import get_weather

wx = get_weather("广州")
# → {"weather": "☀️ 晴朗", "temp": "28°C", ...}
```

### `components/map.py` — 地图组件

```python
from components.map import render_map, build_map_markers

# 构建标记
markers = build_map_markers(dest_coords, "北京", pois_by_cat)

# 渲染地图 HTML
html = render_map(116.404, 39.915, markers, height=500)
```

### `components/poi.py` — POI 卡片组件

```python
from components.poi import render_poi_grid, get_pexels_photo

# 获取真实照片
photo_url = get_pexels_photo("故宫")

# 渲染卡片网格
cards_html = render_poi_grid(pois, 116.404, 39.915)
```

### `components/styles.py` — CSS 主题

```python
from components.styles import get_custom_css

st.markdown(get_custom_css(), unsafe_allow_html=True)
```

---

## 开发规范

### 代码风格

- **格式化**：`black .`（行宽 100）
- **Lint**：`ruff check .`
- **命名**：snake_case（函数/变量）、UPPER_CASE（常量）
- **注释**：中文文档字符串 + 英文代码注释

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: 添加新功能
fix: 修复 Bug
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 重构
test: 测试相关
chore: 构建/工具
```

### 测试规范

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_services.py -v

# 查看覆盖率
pytest tests/ --cov=. --cov-report=html
```

---

## 添加新功能

### 1. 添加新的 API 服务

```python
# services/new_service.py
import requests
from config import SOME_API_KEY

def call_new_api(param):
    if not SOME_API_KEY:
        return None
    try:
        # API 调用逻辑
        pass
    except Exception:
        return None
```

### 2. 添加新的 UI 组件

```python
# components/new_component.py
def render_new_component(data):
    html = f"""..."""
    return html
```

### 3. 在 UI 中集成

```python
# streamlit_app.py
from services.new_service import call_new_api
from components.new_component import render_new_component

data = call_new_api(param)
st.components.v1.html(render_new_component(data))
```

### 4. 添加测试

```python
# tests/test_new_service.py
class TestNewService:
    @patch("services.new_service.requests.get")
    def test_call_success(self, mock_get):
        ...
```

---

## 调试技巧

### Streamlit 调试

```python
# 在 streamlit_app.py 中添加调试输出
st.write("Debug:", variable)
st.json(data)
```

### 日志

Streamlit 默认输出日志到终端（启动 Streamlit 的命令行窗口）。

### 常见问题

**Q: `st.secrets` 读取失败？**
- 检查 `.streamlit/secrets.toml` 是否存在
- 或设置环境变量 `.env`

**Q: 百度地图 API 返回空？**
- 检查 `BAIDU_MAP_AK` 是否正确
- 检查 API 配额是否用完
- 检查网络是否能访问百度地图 API

**Q: LLM 调用超时？**
- 检查 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`
- 检查网络是否能访问 TokenHub
