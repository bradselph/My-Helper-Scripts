@echo off
setlocal

:: Get the directory where the batch script is located
set "folder_path=%~dp0"

:: Set the name of the output file
set "output_file=%folder_path%file_list.txt"

:: Change to the directory where the batch script is located
cd /d "%folder_path%"

:: List files and save to the output file
dir /b /a-d > "%output_file%"

echo File names saved to %output_file%

endlocal
