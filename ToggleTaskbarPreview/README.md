# Taskbar Preview Toggle Script

## Description

The **Taskbar Preview Toggle Script** is a PowerShell script designed to enable or disable the taskbar preview window feature in Windows. This feature shows a preview of open windows when you hover over their icons on the taskbar. This script allows users to quickly toggle this feature on or off based on their preference.

### Features

- **Admin Privileges:** The script automatically checks if it is running with administrative rights. If not, it restarts itself with elevated privileges to ensure it can make the necessary system changes.
- **User Input:** Prompts the user to choose whether to enable or disable the taskbar preview window.
- **Registry Modification:** Modifies the Windows Registry to adjust the taskbar preview settings.
- **Explorer Restart:** Restarts Windows Explorer to apply the changes immediately.
- **User Notification:** Informs the user of the action taken and prompts them to press Enter to close the script, ensuring they see the outcome before exiting.

### How It Works

1. **Admin Check:** The script first checks if it is running with administrative privileges. If not, it restarts itself with elevated permissions.
2. **User Prompt:** Once running as an administrator, the script prompts the user to input their preference: 'disable' to turn off the taskbar preview window or 'enable' to turn it on.
3. **Registry Update:** Based on user input, the script updates the Windows Registry to enable or disable the taskbar preview window.
4. **Restart Explorer:** The script restarts Windows Explorer to apply the changes immediately.
5. **Final Notification:** The script provides feedback to the user about the action taken and waits for them to press Enter before closing.

### Usage

1. Save the script as `ToggleTaskbarPreview.ps1`.
2. Double-click the script file to run it. If administrative rights are required, the script will prompt for elevation.
3. Follow the on-screen instructions to either enable or disable the taskbar preview window.
4. After the changes are applied, press Enter to close the script window.

### Notes

- **Administrative Rights:** The script requires administrative privileges to modify system settings. Ensure you run it with the necessary permissions.
- **Restart Required:** For the changes to take full effect, you may need to restart your computer.
