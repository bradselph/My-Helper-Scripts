# File Mover Script

## Description

The **File Mover Script** is a Python script that relocates all files from subdirectories to the root directory of a specified folder and removes any empty directories left behind. This script is useful for reorganizing directory structures by consolidating files into a single directory.

## Features

- **File Relocation:** Moves all files from subdirectories to the root directory.
- **Empty Directory Removal:** Deletes any empty directories after moving files.
- **User Confirmation:** Prompts the user to confirm the operation before proceeding.
- **Current Directory Usage:** Uses the current working directory as the root folder by default.

## How It Works

1. **Warning Message:** Displays a warning message about the operation to ensure the user is aware of the changes that will be made.
2. **User Confirmation:** Asks the user to confirm whether they want to proceed with the operation.
3. **File Movement:** If confirmed, moves all files from subdirectories to the root directory of the current working directory.
4. **Directory Cleanup:** Removes any empty directories after the files have been moved.
5. **Completion Message:** Notifies the user upon completion or if the operation is canceled.

## Usage

1. **Save the Script:** Copy the script into a file named `file_mover.py`.
2. **Run the Script:** Open a terminal or command prompt and navigate to the directory where the script is saved. Run the script using:
   ```bash
   python file_mover.py
   ```
3. **Confirm Operation:** The script will display a warning message and ask for confirmation. Type `yes` to proceed or `no` to cancel the operation.
4. **Review Results:** If the operation is confirmed, all files from subdirectories will be moved to the root directory, and any empty directories will be removed. The script will display a completion message.

## Example

If the current working directory structure is:

```
root/
├── subdir1/
│   └── file1.txt
├── subdir2/
│   ├── file2.txt
│   └── file3.txt
└── subdir3/
    └── file4.txt
```

After running the script and confirming the operation, the directory structure will be:

```
root/
├── file1.txt
├── file2.txt
├── file3.txt
└── file4.txt
```

And the subdirectories `subdir1`, `subdir2`, and `subdir3` will be removed if they are empty.

## Notes

- **Backup:** Ensure that you have backups of important data before running the script, as the operation cannot be undone.
- **Current Directory:** By default, the script uses the current working directory as the root folder. If you need to specify a different folder, modify the script accordingly.
