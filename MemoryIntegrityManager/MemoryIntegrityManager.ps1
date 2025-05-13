if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This script needs administrator privileges to make system changes." -ForegroundColor Yellow
    Write-Host "Restarting script with administrator privileges..." -ForegroundColor Yellow
    
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

function Show-Menu {
    Clear-Host
    Write-Host "===== Memory Integrity Management Tool =====" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This tool helps you manage Memory Integrity (Core Isolation)" -ForegroundColor White
    Write-Host "settings on your Windows system." -ForegroundColor White
    Write-Host ""
    Write-Host "Current Status:" -ForegroundColor Cyan
    
    $status = Get-MemoryIntegrityStatus
    
    if ($status -eq "Enabled" -or $status -eq "Running") {
        Write-Host "Memory Integrity is ENABLED" -ForegroundColor Green
        Write-Host "Suggested action: Disable (if experiencing compatibility issues)" -ForegroundColor Yellow
    } elseif ($status -eq "Disabled") {
        Write-Host "Memory Integrity is DISABLED" -ForegroundColor Yellow
        Write-Host "Suggested action: Enable (for improved security)" -ForegroundColor Green
    } else {
        Write-Host "Memory Integrity status could not be determined" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Select an option:" -ForegroundColor Cyan
    Write-Host "1. Enable Memory Integrity (improves security, requires restart)" -ForegroundColor Green
    Write-Host "2. Disable Memory Integrity (fixes driver compatibility issues)" -ForegroundColor Yellow
    Write-Host "3. Exit" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-3)"
    return $choice
}

function Get-MemoryIntegrityStatus {
    $status = "Unknown"
    try {
        $regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity"
        if (Test-Path $regPath) {
            $hvciEnabled = Get-ItemProperty -Path $regPath -Name "Enabled" -ErrorAction SilentlyContinue
            
            if ($null -ne $hvciEnabled) {
                if ($hvciEnabled.Enabled -eq 1) {
                    $status = "Enabled"
                } else {
                    $status = "Disabled"
                }
            }
        }
        
        try {
            $deviceGuard = Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard -ErrorAction SilentlyContinue
            
            if ($null -ne $deviceGuard) {
                $securityServicesRunning = $deviceGuard.SecurityServicesRunning
                $hvciRunning = ($securityServicesRunning -band 2) -eq 2
                
                if ($hvciRunning) {
                    $status = "Running"
                }
            }
        } catch {
        }
        
    } catch {
    }
    
    return $status
}

function Check-SystemCompatibility {
    $systemSupported = $true
    $reasonUnsupported = ""

    try {
        $processorInfo = Get-WmiObject -Class Win32_Processor
        $virtualizationFirmwareEnabled = $processorInfo.VirtualizationFirmwareEnabled

        if ($null -eq $virtualizationFirmwareEnabled -or $virtualizationFirmwareEnabled -eq $false) {
            $systemSupported = $false
            $reasonUnsupported = "Hardware virtualization is not enabled in your BIOS/UEFI."
        }
    } catch {
        Write-Host "Warning: Could not verify processor virtualization support." -ForegroundColor Yellow
    }

    if ($systemSupported) {
        try {
            $hyperVFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -ErrorAction SilentlyContinue
            if ($null -eq $hyperVFeature -or $hyperVFeature.State -ne "Enabled") {
                Write-Host "Note: Hyper-V is not enabled, but Memory Integrity may still work." -ForegroundColor Yellow
            }
        } catch {
        }
    }

    return @{
        Supported = $systemSupported
        Reason = $reasonUnsupported
    }
}

function Enable-MemoryIntegrity {
    Clear-Host
    Write-Host "===== Enabling Memory Integrity =====" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Memory Integrity provides enhanced security for your system by protecting" -ForegroundColor White
    Write-Host "Windows from malicious code injection and kernel memory attacks." -ForegroundColor White
    Write-Host ""
    
    Write-Host "Checking if your system supports Memory Integrity..." -ForegroundColor Cyan
    $compatibility = Check-SystemCompatibility
    
    if (-not $compatibility.Supported) {
        Write-Host ""
        Write-Host "Your system may not fully support Memory Integrity: $($compatibility.Reason)" -ForegroundColor Red
        Write-Host "Would you like to try enabling it anyway? This might require BIOS changes." -ForegroundColor Yellow
        $tryAnyway = Read-Host "Continue anyway? (Y/N)"
        
        if ($tryAnyway -ne 'Y' -and $tryAnyway -ne 'y') {
            return $false
        }
    }
    
    $status = Get-MemoryIntegrityStatus
    
    if ($status -eq "Enabled" -or $status -eq "Running") {
        Write-Host ""
        Write-Host "Memory Integrity is already enabled on this system." -ForegroundColor Green
        Write-Host "No further action is needed."
        return $true
    }
    
    Write-Host ""
    Write-Host "IMPORTANT:" -ForegroundColor Yellow
    Write-Host "- Enabling Memory Integrity may cause incompatibility with certain drivers" -ForegroundColor Yellow
    Write-Host "- Your system will need to restart for changes to take effect" -ForegroundColor Yellow
    Write-Host "- If you experience problems after enabling, you can use this tool to disable it" -ForegroundColor Yellow
    Write-Host "- In case of boot failures, you may need to use Windows Recovery Environment" -ForegroundColor Yellow
    Write-Host ""
    
    $confirmation = Read-Host "Do you want to continue? (Y/N)"
    if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
        Write-Host "Operation cancelled by user." -ForegroundColor Yellow
        return $false
    }
    
    $success = $false
    Write-Host ""
    Write-Host "Enabling Memory Integrity..." -ForegroundColor Cyan
    
    try {
        $dgPath = "HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard"
        if (-not (Test-Path $dgPath)) {
            New-Item -Path $dgPath -Force | Out-Null
        }
        
        Set-ItemProperty -Path $dgPath -Name "EnableVirtualizationBasedSecurity" -Value 1 -Type DWord -Force
        
        Set-ItemProperty -Path $dgPath -Name "RequirePlatformSecurityFeatures" -Value 1 -Type DWord -Force
        
        Set-ItemProperty -Path $dgPath -Name "Locked" -Value 0 -Type DWord -Force
        
        $regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity"
        if (-not (Test-Path $regPath)) {
            New-Item -Path $regPath -Force | Out-Null
        }
        
        Set-ItemProperty -Path $regPath -Name "Enabled" -Value 1 -Type DWord -Force
        
        Set-ItemProperty -Path $regPath -Name "Locked" -Value 0 -Type DWord -Force
        
        Set-ItemProperty -Path $regPath -Name "WasEnabledBy" -Value 2 -Type DWord -Force
        
        $success = $true
        Write-Host "Memory Integrity has been successfully enabled." -ForegroundColor Green
    } catch {
        Write-Host "Error enabling Memory Integrity: $_" -ForegroundColor Red
        Write-Host "Trying alternate method..." -ForegroundColor Yellow
        
        try {
            $commands = @(
                'reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v "EnableVirtualizationBasedSecurity" /t REG_DWORD /d 1 /f',
                'reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v "RequirePlatformSecurityFeatures" /t REG_DWORD /d 1 /f',
                'reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v "Locked" /t REG_DWORD /d 0 /f',
                'reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v "Enabled" /t REG_DWORD /d 1 /f',
                'reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v "Locked" /t REG_DWORD /d 0 /f',
                'reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v "WasEnabledBy" /t REG_DWORD /d 2 /f'
            )
            
            $allSucceeded = $true
            foreach ($cmd in $commands) {
                $result = cmd /c $cmd
                if ($LASTEXITCODE -ne 0) {
                    $allSucceeded = $false
                    Write-Host "Command failed: $cmd" -ForegroundColor Red
                }
            }
            
            if ($allSucceeded) {
                $success = $true
                Write-Host "Memory Integrity has been successfully enabled using alternate method." -ForegroundColor Green
            } else {
                Write-Host "Alternate method failed" -ForegroundColor Red
            }
        } catch {
            Write-Host "Error with alternate method: $_" -ForegroundColor Red
        }
    }
    
    if (-not $success) {
        Write-Host ""
        Write-Host "Automatic enabling failed. You can enable Memory Integrity manually:" -ForegroundColor Red
        Write-Host "1. Open Windows Security" -ForegroundColor Yellow
        Write-Host "2. Go to Device Security > Core isolation details" -ForegroundColor Yellow
        Write-Host "3. Turn on Memory integrity" -ForegroundColor Yellow
        return $false
    }
    
    Write-Host ""
    Write-Host "IMPORTANT: Some drivers may be incompatible with Memory Integrity." -ForegroundColor Yellow
    Write-Host "If you experience blue screens or hardware issues after restart," -ForegroundColor Yellow
    Write-Host "you can use this tool again to disable Memory Integrity." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Recovery information:" -ForegroundColor Cyan
    Write-Host "If you cannot boot normally, you can access Windows Recovery Environment," -ForegroundColor White
    Write-Host "open Command Prompt, and run the following command:" -ForegroundColor White
    Write-Host 'reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v "Enabled" /t REG_DWORD /d 0 /f' -ForegroundColor Yellow
    Write-Host ""
    
    return $success
}

function Disable-MemoryIntegrity {
    Clear-Host
    Write-Host "===== Disabling Memory Integrity =====" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This will disable Memory Integrity (Core Isolation)," -ForegroundColor White
    Write-Host "which might be necessary if you're experiencing compatibility issues" -ForegroundColor White
    Write-Host "with certain drivers or applications." -ForegroundColor White
    Write-Host ""
    
    $status = Get-MemoryIntegrityStatus
    
    if ($status -eq "Disabled") {
        Write-Host ""
        Write-Host "Memory Integrity is already disabled on this system." -ForegroundColor Green
        Write-Host "No further action is needed."
        return $true
    }
    
    Write-Host ""
    Write-Host "WARNING: Disabling Memory Integrity will reduce system security protection." -ForegroundColor Yellow
    Write-Host "This should only be done if you're experiencing compatibility problems." -ForegroundColor Yellow
    Write-Host "You may need to restart your computer for changes to take effect." -ForegroundColor Yellow
    Write-Host ""
    
    $confirmation = Read-Host "Do you want to continue? (Y/N)"
    if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
        Write-Host "Operation cancelled by user." -ForegroundColor Yellow
        return $false
    }
    
    $success = $false
    Write-Host ""
    Write-Host "Disabling Memory Integrity..." -ForegroundColor Cyan
    
    try {
        $regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity"
        if (-not (Test-Path $regPath)) {
            New-Item -Path $regPath -Force | Out-Null
        }
        
        Set-ItemProperty -Path $regPath -Name "Enabled" -Value 0 -Type DWord -Force
        
        $vbsPath = "HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard"
        if (Test-Path $vbsPath) {
            Set-ItemProperty -Path $vbsPath -Name "EnableVirtualizationBasedSecurity" -Value 0 -Type DWord -Force
        }
        
        $success = $true
        Write-Host "Memory Integrity has been successfully disabled." -ForegroundColor Green
    } catch {
        Write-Host "Error disabling Memory Integrity: $_" -ForegroundColor Red
        Write-Host "Trying alternate method..." -ForegroundColor Yellow
        
        try {
            $result = cmd /c "reg add ""HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity"" /v ""Enabled"" /t REG_DWORD /d 0 /f"
            $result2 = cmd /c "reg add ""HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard"" /v ""EnableVirtualizationBasedSecurity"" /t REG_DWORD /d 0 /f"
            
            if ($LASTEXITCODE -eq 0) {
                $success = $true
                Write-Host "Memory Integrity has been successfully disabled using alternate method." -ForegroundColor Green
            } else {
                Write-Host "Alternate method failed with exit code: $LASTEXITCODE" -ForegroundColor Red
            }
        } catch {
            Write-Host "Error with alternate method: $_" -ForegroundColor Red
        }
    }
    
    if (-not $success) {
        Write-Host ""
        Write-Host "Automatic disabling failed. You can disable Memory Integrity manually:" -ForegroundColor Red
        Write-Host "1. Open Windows Security" -ForegroundColor Yellow
        Write-Host "2. Go to Device Security > Core isolation details" -ForegroundColor Yellow
        Write-Host "3. Turn off Memory integrity" -ForegroundColor Yellow
        return $false
    }
    
    return $success
}

function Prompt-ForRestart {
    param (
        [string]$Action
    )
    
    Write-Host ""
    $restart = Read-Host "A system restart is required for the changes to take effect. Would you like to restart now? (Y/N)"
    if ($restart -eq 'Y' -or $restart -eq 'y') {
        Write-Host "Restarting computer in 10 seconds. Press Ctrl+C to cancel." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        Restart-Computer -Force
    } else {
        Write-Host "Please restart your computer manually for changes to take effect." -ForegroundColor Yellow
        Write-Host "Memory Integrity changes will not be active until after a restart." -ForegroundColor Yellow
    }
}

$exitRequested = $false

while (-not $exitRequested) {
    $choice = Show-Menu
    
    switch ($choice) {
        "1" {
            $success = Enable-MemoryIntegrity
            if ($success) {
                Prompt-ForRestart -Action "enable"
            }
            
            Write-Host ""
            Write-Host "Press Enter to return to the main menu..." -ForegroundColor Cyan
            Read-Host
        }
        "2" {
            $success = Disable-MemoryIntegrity
            if ($success) {
                Prompt-ForRestart -Action "disable"
            }
            
            Write-Host ""
            Write-Host "Press Enter to return to the main menu..." -ForegroundColor Cyan
            Read-Host
        }
        "3" {
            $exitRequested = $true
            Write-Host "Exiting..." -ForegroundColor Cyan
        }
        default {
            Write-Host "Invalid option. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}