@echo off
cd /d "%~dp0"
python -m streamlit run app.py --server.headless true --server.port 8501 --server.address 127.0.0.1
