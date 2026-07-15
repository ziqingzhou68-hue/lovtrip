"""UI 组件单元测试

测试地图渲染和 POI 卡片组件（纯函数，不依赖 Streamlit）。
"""
import sys
from unittest.mock import patch, MagicMock

import pytest

# 模拟 streamlit
sys.modules["streamlit"] = MagicMock()


class TestBuildMapMarkers:
    """测试地图标记构建"""

    def test_build_markers_empty_pois(self):
        """测试空 POI 时只返回目的地标记"""
        from components.map import build_map_markers

        dest_coords = {"lng": 116.404, "lat": 39.915}
        pois_by_cat = {"景点": [], "酒店": [], "美食": []}

        markers = build_map_markers(dest_coords, "北京", pois_by_cat)
        assert len(markers) == 1
        assert markers[0]["name"] == "北京"
        assert markers[0]["isDest"] is True
        assert markers[0]["lng"] == 116.404
        assert markers[0]["lat"] == 39.915

    def test_build_markers_with_pois(self):
        """测试带 POI 时正确构建标记"""
        from components.map import build_map_markers

        dest_coords = {"lng": 116.404, "lat": 39.915}
        pois_by_cat = {
            "景点": [
                {
                    "name": "故宫",
                    "address": "东城区",
                    "location": {"lng": 116.397, "lat": 39.918},
                    "score": "95",
                }
            ],
            "酒店": [],
            "美食": [
                {
                    "name": "全聚德",
                    "address": "前门",
                    "location": {"lng": 116.398, "lat": 39.900},
                    "score": "90",
                }
            ],
        }

        markers = build_map_markers(dest_coords, "北京", pois_by_cat)
        # 1 destination + 1 spot + 1 food = 3 markers
        assert len(markers) == 3
        # 检查景点标记
        spot_marker = [m for m in markers if m["name"] == "故宫"][0]
        assert spot_marker["color"] == "#ef4444"
        assert spot_marker["isDest"] is False
        # 检查美食标记
        food_marker = [m for m in markers if m["name"] == "全聚德"][0]
        assert food_marker["color"] == "#10b981"

    def test_build_markers_limit_6_per_category(self):
        """测试每类 POI 最多 6 个标记"""
        from components.map import build_map_markers

        dest_coords = {"lng": 116.404, "lat": 39.915}
        # 创建 10 个景点
        spots = [
            {
                "name": f"景点{i}",
                "location": {"lng": 116.4 + i * 0.01, "lat": 39.9 + i * 0.01},
            }
            for i in range(10)
        ]
        pois_by_cat = {"景点": spots, "酒店": [], "美食": []}

        markers = build_map_markers(dest_coords, "北京", pois_by_cat)
        # 1 destination + 6 spots (capped) = 7
        spot_markers = [m for m in markers if not m["isDest"]]
        assert len(spot_markers) <= 6


class TestRenderPOIGrid:
    """测试 POI 卡片渲染"""

    def test_render_empty_pois(self):
        """测试空 POI 时返回提示信息"""
        from components.poi import render_poi_grid

        html = render_poi_grid([], 116.404, 39.915)
        assert "输入目的地" in html or "搜索周边" in html

    def test_render_pois_generates_cards(self):
        """测试 POI 列表生成卡片 HTML"""
        from components.poi import render_poi_grid

        pois = [
            {
                "name": "故宫",
                "address": "北京市东城区",
                "score": "95",
                "price": "60",
                "location": {"lng": 116.397, "lat": 39.918},
            },
            {
                "name": "天坛",
                "address": "北京市东城区",
                "score": "90",
                "price": "15",
                "location": {"lng": 116.411, "lat": 39.882},
            },
        ]

        html = render_poi_grid(pois, 116.404, 39.915)
        assert "poi-card" in html
        assert "故宫" in html
        assert "天坛" in html

    def test_render_pois_truncation(self):
        """测试超过 9 个 POI 时截断"""
        from components.poi import render_poi_grid

        pois = [{"name": f"景点{i}", "location": {"lng": 116.4, "lat": 39.9}} for i in range(20)]

        html = render_poi_grid(pois, 116.404, 39.915)
        # 应该只渲染 9 个卡片
        card_count = html.count("poi-card")
        assert card_count <= 9


class TestRenderMap:
    """测试地图 HTML 渲染"""

    def test_render_map_basic(self):
        """测试基本地图渲染"""
        from components.map import render_map

        html = render_map(116.404, 39.915)
        assert "leaflet" in html.lower()
        assert "OpenStreetMap" in html or "CartoDB" in html or "CARTO" in html
        assert "116.404" in html or "39.915" in html

    def test_render_map_with_markers(self):
        """测试带标记的地图渲染"""
        from components.map import render_map

        markers = [
            {
                "lng": 116.397,
                "lat": 39.918,
                "name": "故宫",
                "addr": "东城区",
                "icon": "🎯",
                "color": "#ef4444",
                "isDest": False,
            }
        ]

        html = render_map(116.404, 39.915, markers)
        assert "故宫" in html

    def test_render_map_custom_height(self):
        """测试自定义高度的地图"""
        from components.map import render_map

        html = render_map(116.404, 39.915, height=600)
        assert "600px" in html or "height:600" in html


class TestGetPexelsPhoto:
    """测试 Pexels 图片获取"""

    @patch("components.poi.requests.get")
    def test_get_photo_success(self, mock_get):
        """测试获取图片成功"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "photos": [{"src": {"medium": "https://example.com/photo.jpg"}}]
        }
        mock_get.return_value = mock_response

        with patch("components.poi.PEXELS_KEY", "test_key"):
            from components.poi import get_pexels_photo
            result = get_pexels_photo("故宫")
            assert result == "https://example.com/photo.jpg"

    def test_get_photo_no_key(self):
        """测试无 API Key 时返回 None"""
        with patch("components.poi.PEXELS_KEY", ""):
            from components.poi import get_pexels_photo
            result = get_pexels_photo("故宫")
            assert result is None

    @patch("components.poi.requests.get")
    def test_get_photo_api_error(self, mock_get):
        """测试 API 错误时返回 None"""
        mock_get.side_effect = Exception("API error")

        with patch("components.poi.PEXELS_KEY", "test_key"):
            from components.poi import get_pexels_photo
            result = get_pexels_photo("故宫")
            assert result is None
