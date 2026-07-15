# LovTrip 部署指南

> Deployment Guide

---

## 部署方式概览

LovTrip 支持多种部署方式：

| 方式 | 难度 | 费用 | 适用场景 |
|------|------|------|----------|
| **Streamlit Cloud** | ⭐ 最简单 | 免费 | 个人使用、课程展示 |
| **本地运行** | ⭐ 简单 | 免费 | 开发调试 |
| **自有服务器** | ⭐⭐ 中等 | 按需 | 生产环境 |

---

## 方式一：Streamlit Cloud 部署（推荐）

### 前提条件

1. GitHub 账号
2. Streamlit Cloud 账号（https://share.streamlit.io/）
3. 代码已推送到 GitHub 仓库

### 步骤

#### 1. 推送代码到 GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/lovtrip.git
git push -u origin main
```

#### 2. 在 Streamlit Cloud 中部署

1. 访问 https://share.streamlit.io/
2. 点击 "New app"
3. 选择仓库：`YOUR_USERNAME/lovtrip`
4. 选择分支：`main`
5. 选择主文件：`streamlit_app.py`
6. 点击 "Deploy"

#### 3. 配置 Secrets

在 Streamlit Cloud 的应用设置中 → Secrets，填入：

```toml
OPENAI_API_KEY = "your_actual_key_here"
OPENAI_BASE_URL = "https://tokenhub.tencentmaas.com/v1/"
MODEL_NAME = "kimi-k2.7-code"
BAIDU_MAP_AK = "your_baidu_ak_here"
PEXELS_API_KEY = "your_pexels_key_here"
```

> ⚠️ 注意：Streamlit Cloud 的 Secrets 值是明文 TOML 格式，与本地 `.streamlit/secrets.toml` 格式相同。

#### 4. 访问应用

部署完成后，Streamlit Cloud 会分配一个 URL（如 `https://your-app.streamlit.app/`）。

---

## 方式二：本地运行

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/lovtrip.git
cd lovtrip

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置
cp .env.example .env
# 编辑 .env，填入真实 API Key

# 或使用 Streamlit Secrets 方式
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# 编辑 secrets.toml

# 4. 启动
streamlit run streamlit_app.py

# 5. 访问
# http://localhost:8501
```

---

## 方式三：自有服务器部署

### 使用 Docker（推荐）

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# 构建
docker build -t lovtrip .

# 运行（传入环境变量）
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  -e BAIDU_MAP_AK=your_ak \
  lovtrip
```

### 使用 systemd（Linux）

```ini
# /etc/systemd/system/lovtrip.service
[Unit]
Description=LovTrip Streamlit App
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/lovtrip
Environment="OPENAI_API_KEY=your_key"
Environment="BAIDU_MAP_AK=your_ak"
ExecStart=/opt/lovtrip/venv/bin/streamlit run streamlit_app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable lovtrip
sudo systemctl start lovtrip
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name lovtrip.example.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 环境变量参考

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `OPENAI_API_KEY` | (必需) | LLM API Key |
| `OPENAI_BASE_URL` | `https://tokenhub.tencentmaas.com/v1/` | LLM API 地址 |
| `MODEL_NAME` | `kimi-k2.7-code` | 模型名称 |
| `BAIDU_MAP_AK` | (必需) | 百度地图 API Key |
| `PEXELS_API_KEY` | (可选) | Pexels 图片 API Key |

---

## 验证部署

部署完成后，进行以下验证：

1. ✅ 访问应用 URL，能看到 LovTrip 主界面
2. ✅ 输入目的地，地图正常加载
3. ✅ 天气信息正常显示
4. ✅ 点击"生成行程"，能收到 AI 回复
5. ✅ POI 探索标签页能显示周边信息

---

## 故障排除

### 应用启动失败

- 检查 Python 版本 ≥ 3.9
- 检查所有依赖已安装：`pip list | grep streamlit`

### 地图不显示

- 检查网络是否能访问 `unpkg.com`（Leaflet CDN）
- 检查浏览器控制台是否有 JavaScript 错误

### LLM 调用失败

- 检查 `OPENAI_API_KEY` 是否正确
- 检查 `OPENAI_BASE_URL` 是否可达
- 检查 API 配额是否用完

### 百度地图 API 无结果

- 检查 `BAIDU_MAP_AK` 是否正确
- 检查百度地图 API 控制台配额
- 国内服务器部署时 IP 白名单是否配置
