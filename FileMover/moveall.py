import os
import shutil

def move_files_to_root(root_folder):
    # Walk through the directory tree
    for root, dirs, files in os.walk(root_folder, topdown=False):
        # Move files from subdirectories to the root directory
        for file_name in files:
            file_path = os.path.join(root, file_name)
            shutil.move(file_path, os.path.join(root_folder, file_name))
        
        # Remove the empty directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if the directory is empty
                os.rmdir(dir_path)

if __name__ == "__main__":
    # Display a warning message
    print("WARNING: This script will move all files from subdirectories to the root directory")
    print("and remove any empty directories. Do you want to proceed? (yes/no)")
    
    # Get user input
    user_input = input().strip().lower()
    
    if user_input == 'yes':
        root_folder = os.getcwd()  # Use current working directory as the root folder
        move_files_to_root(root_folder)
        print("Files have been moved to the root directory and empty folders have been removed.")
    else:
        print("Operation cancelled.")
