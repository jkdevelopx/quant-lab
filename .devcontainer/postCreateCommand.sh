#!/bin/bash
echo "Installing QuantLab dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt --quiet
echo "All set! Run: streamlit run streamlit_app.py --server.port 8501"
