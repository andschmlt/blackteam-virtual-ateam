# Setup Second Screen - 6 Claude Code Windows
# Layout: 6 columns on ultrawide secondary monitor

# Wait for monitors to be ready (important for startup)
param(
    [int]$StartupDelay = 0  # Set to 10-15 for startup scenarios
)

if ($StartupDelay -gt 0) {
    Write-Host "Waiting $StartupDelay seconds for monitors to initialize..."
    Start-Sleep -Seconds $StartupDelay
}

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class WindowManager {
    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);

    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
}
"@

# ============================================
# CONFIGURATION
# ============================================

# Working directories for each Claude instance (customize as needed)
$claudeConfigs = @(
    @{ Name = "Claude 1"; WorkDir = "C:\Users\andre" },
    @{ Name = "Claude 2"; WorkDir = "C:\Users\andre" },
    @{ Name = "Claude 3"; WorkDir = "C:\Users\andre" },
    @{ Name = "Claude 4"; WorkDir = "C:\Users\andre" },
    @{ Name = "Claude 5"; WorkDir = "C:\Users\andre" },
    @{ Name = "Claude 6"; WorkDir = "C:\Users\andre" }
)

# ============================================
# DETECT SECOND MONITOR
# ============================================

Add-Type -AssemblyName System.Windows.Forms
$screens = [System.Windows.Forms.Screen]::AllScreens

Write-Host "`n=== MONITOR DETECTION ===" -ForegroundColor Cyan

if ($screens.Count -lt 2) {
    Write-Host "ERROR: No second monitor found!" -ForegroundColor Red
    Write-Host "Available monitors:"
    $screens | ForEach-Object { Write-Host "  - $($_.DeviceName) $(if($_.Primary){'(Primary)'})" }
    exit 1
}

# Get the NON-PRIMARY monitor (second screen)
$secondMonitor = $screens | Where-Object { -not $_.Primary } | Select-Object -First 1

# Monitor coordinates
$X = $secondMonitor.WorkingArea.X
$Y = $secondMonitor.WorkingArea.Y
$W = $secondMonitor.WorkingArea.Width
$H = $secondMonitor.WorkingArea.Height

Write-Host "Second Monitor: $($secondMonitor.DeviceName)"
Write-Host "Position: X=$X, Y=$Y"
Write-Host "Size: ${W} x ${H}"

# ============================================
# CALCULATE 6 VERTICAL SPLITS
# ============================================

$numZones = 6
$zoneWidth = [math]::Floor($W / $numZones)
$zoneHeight = $H

Write-Host "`n=== ZONE CALCULATION ===" -ForegroundColor Cyan
Write-Host "Splitting into $numZones vertical columns"
Write-Host "Each zone: ${zoneWidth} x ${zoneHeight} pixels"

$zones = @()
for ($i = 0; $i -lt $numZones; $i++) {
    $zoneX = $X + ($i * $zoneWidth)
    $zones += @{ X = $zoneX; Y = $Y; W = $zoneWidth; H = $zoneHeight }
    Write-Host "  Zone $($i+1): X=$zoneX"
}

Write-Host "`nLayout:" -ForegroundColor Yellow
Write-Host "+--------+--------+--------+--------+--------+--------+"
Write-Host "|Claude 1|Claude 2|Claude 3|Claude 4|Claude 5|Claude 6|"
Write-Host "+--------+--------+--------+--------+--------+--------+"

# ============================================
# LAUNCH 6 WINDOWS TERMINAL WITH CLAUDE
# ============================================

Write-Host "`n=== LAUNCHING CLAUDE WINDOWS ===" -ForegroundColor Cyan

$processes = @()

for ($i = 0; $i -lt $claudeConfigs.Count; $i++) {
    $config = $claudeConfigs[$i]
    Write-Host "Starting $($config.Name)..."

    try {
        # Launch Windows Terminal with Ubuntu profile, then run claude
        # -w new = new window (not tab)
        # -p "Ubuntu" = use Ubuntu profile
        # -- bash -lic "claude" = run claude in login shell
        Start-Process -FilePath "cmd.exe" `
            -ArgumentList "/c start wt.exe -w new -p Ubuntu --title `"$($config.Name)`" -- bash -lic claude" `
            -WindowStyle Hidden

        # Longer stagger to ensure windows fully spawn
        Start-Sleep -Milliseconds 2000
    }
    catch {
        Write-Host "  FAILED: $_" -ForegroundColor Red
    }
}

# Wait for windows to fully open
Write-Host "`nWaiting 6 seconds for Claude windows to initialize..."
Start-Sleep -Seconds 6

# ============================================
# POSITION WINDOWS
# ============================================

Write-Host "`n=== POSITIONING WINDOWS ===" -ForegroundColor Cyan

# We need to enumerate all windows since Windows Terminal is single-process
Add-Type @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

public class WindowEnumerator {
    [DllImport("user32.dll")]
    private static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

    [DllImport("user32.dll")]
    private static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    private static extern int GetWindowTextLength(IntPtr hWnd);

    [DllImport("user32.dll")]
    private static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    private static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);

    private delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    public static List<IntPtr> GetWindowsTerminalWindows() {
        List<IntPtr> windows = new List<IntPtr>();

        EnumWindows((hWnd, lParam) => {
            if (IsWindowVisible(hWnd)) {
                StringBuilder className = new StringBuilder(256);
                GetClassName(hWnd, className, className.Capacity);

                // Windows Terminal uses CASCADIA_HOSTING_WINDOW_CLASS
                if (className.ToString().Contains("CASCADIA_HOSTING_WINDOW_CLASS")) {
                    windows.Add(hWnd);
                }
            }
            return true;
        }, IntPtr.Zero);

        return windows;
    }
}
"@

$wtWindows = [WindowEnumerator]::GetWindowsTerminalWindows()
Write-Host "Found $($wtWindows.Count) Windows Terminal windows"

# Position each window
$positioned = 0
foreach ($hwnd in $wtWindows) {
    if ($positioned -ge $numZones) { break }

    $zone = $zones[$positioned]

    if ($hwnd -ne [IntPtr]::Zero) {
        # Restore window first
        [WindowManager]::ShowWindow($hwnd, 9) | Out-Null
        Start-Sleep -Milliseconds 100

        # Move to zone
        $result = [WindowManager]::MoveWindow($hwnd, $zone.X, $zone.Y, $zone.W, $zone.H, $true)

        if ($result) {
            Write-Host "OK: Window $($positioned + 1) -> Zone $($positioned + 1)" -ForegroundColor Green
            $positioned++
        } else {
            Write-Host "WARN: Window move may have failed" -ForegroundColor Yellow
        }
    }
}

Write-Host "`n=== DONE ===" -ForegroundColor Green
Write-Host "$positioned Claude windows positioned on second monitor"

if ($positioned -lt $numZones) {
    Write-Host "`nTIP: If some windows weren't positioned, try running again." -ForegroundColor Yellow
    Write-Host "     Windows Terminal may take longer to initialize." -ForegroundColor Yellow
}
