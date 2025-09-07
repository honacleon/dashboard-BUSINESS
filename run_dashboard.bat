@echo off
echo ===========================================
echo    🏆 GOLD BUSINESS DASHBOARD PREMIUM
echo ===========================================
echo.
echo Iniciando o dashboard executivo...
echo.
echo 📊 Dashboard URL: http://localhost:8502
echo 👥 Usuários Demo:
echo   - Admin:   goldadmin / admin123
echo   - Manager: goldmanager / manager123  
echo   - Viewer:  goldviewer / viewer123
echo.
echo Pressione Ctrl+C para parar o dashboard
echo ===========================================
echo.

python -m streamlit run main.py --server.port 8502

pause