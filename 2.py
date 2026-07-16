"""LovTrip 入口 — 重定向到 streamlit_app.py"""
import os
_path = os.path.join(os.path.dirname(__file__), 'streamlit_app.py')
with open(_path, encoding='utf-8') as f:
    exec(compile(f.read(), _path, 'exec'))
