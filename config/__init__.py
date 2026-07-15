"""LovTrip 全局配置模块

读取 API Key 配置：优先 Streamlit Secrets，回退到环境变量。
"""

import os
import streamlit as st


def get_config(key, default=""):
    """读取配置：优先 st.secrets，回退到环境变量

    Args:
        key: 配置键名（如 OPENAI_API_KEY）
        default: 默认值

    Returns:
        配置值
    """
    try:
        return st.secrets[key]
    except (KeyError, AttributeError):
        return os.environ.get(key, default)


# ── LLM 配置 ──
API_KEY = get_config("OPENAI_API_KEY")
BASE_URL = get_config("OPENAI_BASE_URL", "https://tokenhub.tencentmaas.com/v1/")
MODEL = get_config("MODEL_NAME", "kimi-k2.7-code")

# ── 第三方 API 配置 ──
BAIDU_AK = get_config("BAIDU_MAP_AK", "")
PEXELS_KEY = get_config("PEXELS_API_KEY", "")

# ── System Prompt ──
SYSTEM_PROMPT = """你是贴心专业、灵活全能的全域旅游规划助手，支持全球任意目的地、完全由用户自主决定出行时长，适配亲子、情侣、闺蜜、独自出行、家庭团建等全人群，可按需适配穷游、轻奢、休闲慢游、特种兵打卡等各类出行模式。

专注定制可直接落地的个性化旅游方案，整合目的地核心资源：精准筛选适配预算与地段的酒店民宿、梳理必游景点小众秘境、深挖本地特色美食老字号门店。

配套完整出行细节：交通接驳、最佳游玩时段、避雷攻略、穿搭建议、注意事项。行程规划时务必结合天气信息：若天气晴好推荐户外景点；若遇雨雪极端天气调整为室内替代方案。

输出格式要求：使用清晰的markdown排版，包含emoji图标、分级标题、重点加粗，让行程方案赏心悦目。"""
