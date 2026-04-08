@echo off
title XenForo Auto Translate - Reset API Key
python "%~dp0xf_translate.py" --reset-key
if %errorlevel% neq 0 (
    echo.
    pause
)
