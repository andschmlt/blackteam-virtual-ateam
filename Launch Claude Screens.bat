@echo off
:: Manual trigger for 6 Claude windows on ultrawide
:: No delay since monitors are already on

powershell.exe -ExecutionPolicy Bypass -File "\\wsl.localhost\Ubuntu\home\andre\setup-claude-screens.ps1" -StartupDelay 0
