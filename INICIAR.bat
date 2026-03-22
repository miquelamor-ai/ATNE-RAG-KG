@echo off
echo ========================================
echo   ATNE - Adaptador de Textos
echo   Jesuites Educacio
echo ========================================
echo.
echo Instal-lant dependencies...
pip install -r requirements.txt -q
echo.
echo Arrencant servidor...
echo Obre el navegador a: http://localhost:8000
echo.
python server.py
pause
