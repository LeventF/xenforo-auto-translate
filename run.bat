@echo off
title XenForo Auto Translate

reg query "HKCU\Console" /v VirtualTerminalLevel >nul 2>&1 || reg add "HKCU\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Download from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python -c "import deepl" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing deepl package...
    python -m pip install deepl --quiet
    python -c "import deepl" >nul 2>&1
    if %errorlevel% neq 0 (
        python -m pip install deepl --user --quiet
    )
)

python "%~dp0xf_translate.py" %*
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. See message above.
    pause
)
