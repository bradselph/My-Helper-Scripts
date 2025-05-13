# Memory Integrity Manager

A PowerShell based utility for managing Memory Integrity (Core Isolation) settings in Windows 10 and 11.

## Overview

Memory Integrity Manager provides an easy to use interface for enabling or disabling Memory Integrity (HVCI - Hypervisor-Enforced Code Integrity)


## Features

- **Status Detection**: Automatically detects current Memory Integrity status
- **Compatibility Check**: Verifies if your system supports Memory Integrity before enabling
- **Administrator Elevation**: Automatically requests administrator privileges when needed
- **Restart Management**: Optional system restart after changes are applied


## Usage

run the Memory Integrity Manager:

1. Open PowerShell as Administrator
2. Navigate to the script location
3. Run `.\MemoryIntegrityManager.ps1`


## How It Works

The utility performs several key functions:

1. **Status Detection**: Uses registry and WMI queries to accurately determine if Memory Integrity is enabled
2. **System Compatibility**: Checks for virtualization support and other requirements
3. **Registry Modification**: Makes the necessary registry changes to enable/disable Memory Integrity
4. **Failover Methods**: Implements multiple methods to ensure changes are applied correctly

## Troubleshooting

### Boot Issues After Enabling Memory Integrity

If you experience boot failures after enabling Memory Integrity:

1. Boot into Windows Recovery Environment (WinRE)
2. Open Command Prompt
3. Run this command to disable Memory Integrity:
   ```
   reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v "Enabled" /t REG_DWORD /d 0 /f
   ```
4. Restart your system