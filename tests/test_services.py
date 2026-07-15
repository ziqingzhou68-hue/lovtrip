"""服务层单元测试

测试天气服务和百度地图 API 服务（使用 Mock，不依赖真实 API）。
"""
import sys
from unittest.mock import patch, MagicMock

import pytest

# 模拟 streamlit
sys.modules["streamlit"] = MagicMock()


class TestBaiduGeocode:
    """测试百度地图地理编码"""

    @patch("services.baidu_map.requests.get")
    def test_geocode_success(self, mock_get):
        """测试地理编码成功返回坐标"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": 0,
            "result": {"location": {"lng": 116.404, "lat": 39.915}},
        }
        mock_get.return_value = mock_response

        # 需要设置 BAIDU_AK 为非空
        with patch("services.baidu_map.BAIDU_AK", "test_ak"):
            from services.baidu_map import baidu_geocode
            result = baidu_geocode("北京")
            assert result is not None
            assert "lng" in result
            assert "lat" in result
            assert result["lng"] == 116.404
            assert result["lat"] == 39.915

    def test_geocode_no_ak(self):
        """测试无 API Key 时返回 None"""
        with patch("services.baidu_map.BAIDU_AK", ""):
            from services.baidu_map import baidu_geocode
            result = baidu_geocode("北京")
            assert result is None

    @patch("services.baidu_map.requests.get")
    def test_geocode_api_error(self, mock_get):
        """测试 API 返回错误状态"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": 1, "message": "error"}
        mock_get.return_value = mock_response

        with patch("services.baidu_map.BAIDU_AK", "test_ak"):
            from services.baidu_map import baidu_geocode
            result = baidu_geocode("invalid")
            assert result is None

    @patch("services.baidu_map.requests.get")
    def test_geocode_network_error(self, mock_get):
        """测试网络异常时返回 None"""
        mock_get.side_effect = Exception("Network error")

        with patch("services.baidu_map.BAIDU_AK", "test_ak"):
            from services.baidu_map import baidu_geocode
            result = baidu_geocode("北京")
            assert result is None


class TestBaiduPlaceSearch:
    """测试百度地图地点搜索"""

    @patch("services.baidu_map.requests.get")
    def test_place_search_success(self, mock_get):
        """测试地点搜索成功返回结果"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": 0,
            "results": [
                {"name": "故宫", "address": "北京市东城区", "location": {"lng": 116.397, "lat": 39.918}},
            ],
        }
        mock_get.return_value = mock_response

        with patch("services.baidu_map.BAIDU_AK", "test_ak"):
            from services.baidu_map import baidu_place_search
            results = baidu_place_search("景点", 116.404, 39.915)
            assert len(results) > 0
            assert results[0]["name"] == "故宫"

    def test_place_search_no_ak(self):
        """测试无 API Key 时返回空列表"""
        with patch("services.baidu_map.BAIDU_AK", ""):
            from services.baidu_map import baidu_place_search
            results = baidu_place_search("景点", 116.404, 39.915)
            assert results == []

    @patch("services.baidu_map.requests.get")
    def test_place_search_api_error(self, mock_get):
        """测试 API 错误时返回空列表"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": 1}
        mock_get.return_value = mock_response

        with patch("services.baidu_map.BAIDU_AK", "test_ak"):
            from services.baidu_map import baidu_place_search
            results = baidu_place_search("景点", 116.404, 39.915)
            assert results == []

    @patch("services.baidu_map.requests.get")
    def test_place_search_network_error(self, mock_get):
        """测试网络异常时返回空列表"""
        mock_get.side_effect = Exception("Timeout")

        with patch("services.baidu_map.BAIDU_AK", "test_ak"):
            from services.baidu_map import baidu_place_search
            results = baidu_place_search("景点", 116.404, 39.915)
            assert results == []


class TestWeatherService:
    """测试天气服务"""

    @patch("services.weather.baidu_geocode")
    @patch("services.weather.requests.get")
    def test_get_weather_success(self, mock_get, mock_geocode):
        """测试天气查询成功"""
        mock_geocode.return_value = {"lng": 116.404, "lat": 39.915}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current_weather": {
                "temperature": 25.0,
                "windspeed": 10.0,
                "weathercode": 0,
            }
        }
        mock_get.return_value = mock_response

        from services.weather import get_weather
        result = get_weather("北京")
        assert result is not None
        assert "weather" in result
        assert "temp" in result
        assert "25" in result["temp"]

    def test_get_weather_geocode_fail(self):
        """测试地理编码失败时返回 None"""
        with patch("services.weather.baidu_geocode", return_value=None):
            from services.weather import get_weather
            result = get_weather("invalid")
            assert result is None
