@echo off
echo Installing dependencies...
pip install streamlit requests pandas streamlit-option-menu python-dotenv

echo.
echo Starting IT Support Assistant...
echo.
echo Opening browser at http://localhost:8501
echo.
python -m streamlit run app.py
