@echo off
:: Vérifie si le script est lancé en admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 🔐 Relancement en mode administrateur...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: Se place dans le répertoire du script
cd /d "%~dp0"

:: Lance le script Python
python interface.py

pause
