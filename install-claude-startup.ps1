# Install Claude Screens to Windows Startup
# This script creates a shortcut in the Startup folder

param(
    [switch]$TaskScheduler,  # Use Task Scheduler instead of Startup folder
    [int]$DelaySeconds = 10  # Delay after login (Task Scheduler only)
)

$scriptPath = Join-Path $PSScriptRoot "setup-claude-screens.bat"

if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: setup-claude-screens.bat not found at $scriptPath" -ForegroundColor Red
    exit 1
}

if ($TaskScheduler) {
    # ============================================
    # OPTION 2: Task Scheduler (with delay)
    # ============================================
    Write-Host "Creating Task Scheduler task..." -ForegroundColor Cyan

    $taskName = "ClaudeScreensStartup"
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    $trigger.Delay = "PT${DelaySeconds}S"  # Delay in ISO 8601 duration format
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

    # Remove existing task if present
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Launch 6 Claude windows on secondary monitor"

    Write-Host "SUCCESS: Task '$taskName' created!" -ForegroundColor Green
    Write-Host "  - Runs at logon with ${DelaySeconds}s delay"
    Write-Host "  - To remove: Unregister-ScheduledTask -TaskName '$taskName'"
}
else {
    # ============================================
    # OPTION 1: Startup Folder (immediate)
    # ============================================
    Write-Host "Creating Startup folder shortcut..." -ForegroundColor Cyan

    $startupFolder = [Environment]::GetFolderPath("Startup")
    $shortcutPath = Join-Path $startupFolder "ClaudeScreens.lnk"

    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $scriptPath
    $shortcut.WorkingDirectory = $PSScriptRoot
    $shortcut.Description = "Launch 6 Claude windows on secondary monitor"
    $shortcut.Save()

    Write-Host "SUCCESS: Shortcut created at:" -ForegroundColor Green
    Write-Host "  $shortcutPath"
    Write-Host ""
    Write-Host "To remove: Delete the shortcut from:"
    Write-Host "  $startupFolder"
}

Write-Host ""
Write-Host "=== INSTALLATION COMPLETE ===" -ForegroundColor Green
