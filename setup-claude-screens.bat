@echo off
:: Launch 6 Claude Code windows on secondary ultrawide monitor
:: Run this at startup or manually

:: Add 15 second delay for startup (monitors need time to initialize)
powershell.exe -ExecutionPolicy Bypass -File "%~dp0setup-claude-screens.ps1" -StartupDelay 15
