"""配置模块测试

测试 config 模块的 API Key 读取和配置管理。
"""
import os
import sys
import importlib
from unittest.mock import patch, MagicMock

import pytest


def _setup_streamlit_mock():
    """设置 streamlit mock，使其 secrets 不可用（回退到 os.environ）"""
    mock_st = MagicMock()
    mock_st.secrets = MagicMock()
    # secrets[key] 抛出 KeyError，secrets.get() 也抛出 KeyError
    mock_st.secrets.__getitem__.side_effect = KeyError
    mock_st.secrets.get.side_effect = KeyError
    # 也处理 AttributeError: st.secrets 存在但返回的配置不存在
    sys.modules["streamlit"] = mock_st
    # 清除 config 模块缓存，强制重新加载
    if "config" in sys.modules:
        del sys.modules["config"]
    return mock_st


class TestConfigLoading:
    """测试配置加载逻辑"""

    def test_get_config_from_env(self):
        """测试从环境变量读取配置"""
        _setup_streamlit_mock()
        with patch.dict(os.environ, {"TEST_KEY": "test_value"}, clear=True):
            import config
            importlib.reload(config)
            result = config.get_config("TEST_KEY", "default")
            assert result == "test_value"

    def test_get_config_default(self):
        """测试配置默认值回退"""
        _setup_streamlit_mock()
        with patch.dict(os.environ, {}, clear=True):
            import config
            importlib.reload(config)
            result = config.get_config("NONEXISTENT_KEY", "fallback")
            assert result == "fallback"

    def test_get_config_empty_default(self):
        """测试空字符串默认值"""
        _setup_streamlit_mock()
        with patch.dict(os.environ, {}, clear=True):
            import config
            importlib.reload(config)
            result = config.get_config("NONEXISTENT_KEY", "")
            assert result == ""

    def test_config_constants_exist(self):
        """测试配置常量存在"""
        _setup_streamlit_mock()
        with patch.dict(os.environ, {}, clear=True):
            import config
            importlib.reload(config)
        assert hasattr(config, "API_KEY")
        assert hasattr(config, "BASE_URL")
        assert hasattr(config, "MODEL")
        assert hasattr(config, "BAIDU_AK")
        assert hasattr(config, "PEXELS_KEY")
        assert hasattr(config, "SYSTEM_PROMPT")

    def test_system_prompt_not_empty(self):
        """测试 SYSTEM_PROMPT 非空"""
        _setup_streamlit_mock()
        with patch.dict(os.environ, {}, clear=True):
            import config
            importlib.reload(config)
        assert len(config.SYSTEM_PROMPT) > 100
        assert "旅游规划" in config.SYSTEM_PROMPT

    def test_default_base_url(self):
        """测试默认 Base URL"""
        _setup_streamlit_mock()
        with patch.dict(os.environ, {}, clear=True):
            import config
            importlib.reload(config)
            result = config.get_config("OPENAI_BASE_URL", "https://tokenhub.tencentmaas.com/v1/")
            assert "tokenhub" in result or "api" in result.lower() or "v1" in result

    def test_default_model_name(self):
        """测试默认模型名称"""
        _setup_streamlit_mock()
        with patch.dict(os.environ, {}, clear=True):
            import config
            importlib.reload(config)
            result = config.get_config("MODEL_NAME", "kimi-k2.7-code")
            assert "kimi" in result.lower() or "k2" in result
