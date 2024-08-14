# Function to restart the script with elevated privileges
function Start-Elevated {
    param (
        [string]$ScriptPath
    )
    $arguments = "& '$ScriptPath'"
    Start-Process powershell -ArgumentList $arguments -Verb runAs
    exit
}

# Check if the script is running as Administrator
function Test-IsAdmin {
    try {
        $adminCheck = [Security.Principal.WindowsIdentity]::GetCurrent().Groups | Where-Object { $_.Value -eq 'S-1-5-32-544' }
        return $adminCheck -ne $null
    } catch {
        return $false
    }
}

if (-not (Test-IsAdmin)) {
    # Restart the script with elevated privileges
    Start-Elevated -ScriptPath $PSCommandPath
}

# Define registry paths and values
$taskbandRegistryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband"
$advancedRegistryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
$valueName = "NumThumbnails"
$hoverTimeValueName = "ExtendedUIHoverTime"

# Prompt user for action
$action = Read-Host "Enter 'disable' to turn off taskbar preview window or 'enable' to turn it on"

# Validate input and set values accordingly
switch ($action.ToLower()) {
    'disable' {
        $valueData = 0
        $hoverTimeValueData = 30000 # Set hover time to 30000 milliseconds
        Write-Output "Disabling taskbar preview window..."
    }
    'enable' {
        $valueData = 1
        $hoverTimeValueData = 0 # Reset hover time
        Write-Output "Enabling taskbar preview window..."
    }
    default {
        Write-Output "Invalid input. Please enter 'disable' or 'enable'."
        Read-Host "Press Enter to exit..."
        exit
    }
}

# Create or update the registry keys
if (-not (Test-Path $taskbandRegistryPath)) {
    New-Item -Path $taskbandRegistryPath -Force | Out-Null
}
Set-ItemProperty -Path $taskbandRegistryPath -Name $valueName -Value $valueData

if (-not (Test-Path $advancedRegistryPath)) {
    New-Item -Path $advancedRegistryPath -Force | Out-Null
}
Set-ItemProperty -Path $advancedRegistryPath -Name $hoverTimeValueName -Value $hoverTimeValueData

# Restart Windows Explorer to apply changes
Stop-Process -Name explorer -Force
Start-Process explorer

Write-Output "Taskbar preview window has been $($action). Please restart your computer for the changes to take full effect."

# Pause to keep the window open
Read-Host "Press Enter to exit..."
