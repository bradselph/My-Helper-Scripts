import os
import subprocess
import sys
import tiktoken
from tqdm import tqdm

def install_package(package_name):
    """Installs a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")
        sys.exit(1)

required_packages = ['tiktoken', 'tqdm']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} library not found. Installing...")
        install_package(package)
    import tiktoken

# Define file extensions to be excluded from content extraction
EXCLUDED_EXTENSIONS = {'.exe', '.dll', '.bin', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', '.pyc', '.pyo'}
EXCLUDED_DIRECTORIES = {'.git', '.github', '.idea', '__pycache__', 
    'node_modules', 'venv', 'env'}
    

# Initialize tokenizer from tiktoken library
tokenizer = tiktoken.get_encoding('o200k_base')

def get_file_contents(filepath):
    """Reads and returns the contents of a file with improved encoding handling."""
    try:
        if os.path.splitext(filepath)[1].lower() in EXCLUDED_EXTENSIONS:
            return "Excluded file type (binary/image)", 0

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            tokens = len(tokenizer.encode(content))
            return content, tokens
    except Exception as e:
        return f"Error reading file {filepath}: {e}", 0

def collect_directory_mapping(startpath):
    """Collects directory mapping of the project."""
    def traverse_directory(root, file, level=0):
        try:
            files = sorted(os.listdir(root))
            for i, f in enumerate(files):
                file_path = os.path.join(root, f)
                if os.path.isdir(file_path):
                    if os.path.basename(file_path) not in EXCLUDED_DIRECTORIES:
                        file.write(f"{'│   ' * level}├── {os.path.basename(file_path)}/\n")
                        traverse_directory(file_path, file, level + 1)
                else:
                    file.write(f"{'│   ' * level}├── {f}\n")
        except Exception as e:
            print(f"Error processing directory {root}: {e}")

    with open('directory.txt', 'w', encoding='utf-8') as file:
        traverse_directory(startpath, file)

def generate_file_contents(startpath):
    """Generates file contents with progress indication."""
    def count_files(path):
        count = 0
        for root, _, files in os.walk(path):
            if os.path.basename(root) not in EXCLUDED_DIRECTORIES:
                count += len(files)
        return count

    total_files = count_files(startpath)
    processed = 0

    with open('codebase.txt', 'w', encoding='utf-8') as out_file:
        def traverse_directory(root):
            nonlocal processed
            try:
                files = sorted(os.listdir(root))
                for f in files:
                    file_path = os.path.join(root, f)
                    if os.path.isdir(file_path):
                        if os.path.basename(file_path) not in EXCLUDED_DIRECTORIES:
                            traverse_directory(file_path)
                    else:
                        content, tokens = get_file_contents(file_path)
                        filename = os.path.basename(file_path)
                        out_file.write(f"<file path='{os.path.relpath(file_path, startpath)}'>\n")
                        out_file.write(f"{content}\n")
                        out_file.write(f"</file>\n")
                        processed += 1
                        print(f"Processing files... {processed}/{total_files}", end='\r')
            except Exception as e:
                print(f"Error processing directory {root}: {e}")

        traverse_directory(startpath)
        print("\nFile processing complete!")

def generate_stats(directory_file, contents_file):
    """Generates a statistics file from directory and contents files."""
    total_files = 0
    total_folders = 0
    total_code_lines = 0
    total_tokens = 0
    processed_files = set()
    all_files = set()
    file_types = {}

    # Process directory file
    with open(directory_file, 'r', encoding='utf-8') as dir_file:
        for line in dir_file:
            line = line.strip()
            if line.endswith('/'):
                total_folders += 1
            else:
                total_files += 1
                filename = line.split('├── ')[1].strip()
                all_files.add(filename)
                ext = os.path.splitext(filename)[1].lower()
                if ext not in EXCLUDED_EXTENSIONS:
                    file_types[ext] = file_types.get(ext, 0) + 1

    # Process contents file
    with open(contents_file, 'r', encoding='utf-8') as content_file:
        inside_tag = False
        current_file = None
        file_lines = []
        for line in content_file:
            if line.startswith('<file path='):
                if inside_tag:
                    total_code_lines += len(file_lines)
                    total_tokens += len(tokenizer.encode(''.join(file_lines)))
                    processed_files.add(current_file)
                current_file = line.split("path='")[1].split("'")[0]
                file_lines = []
                inside_tag = True
            elif line.startswith('</file>'):
                total_code_lines += len(file_lines)
                total_tokens += len(tokenizer.encode(''.join(file_lines)))
                processed_files.add(current_file)
                inside_tag = False
            elif inside_tag:
                file_lines.append(line)

        if inside_tag:
            total_code_lines += len(file_lines)
            total_tokens += len(tokenizer.encode(''.join(file_lines)))
            processed_files.add(current_file)

    excluded_files = {f for f in all_files if os.path.splitext(f)[1].lower() in EXCLUDED_EXTENSIONS}

    # Write statistics
    with open('stats.txt', 'w', encoding='utf-8') as stats_file:
        stats_file.write("Project Statistics\n")
        stats_file.write("=================\n\n")
        stats_file.write(f"Total files: {total_files}\n")
        stats_file.write(f"Total folders: {total_folders}\n")
        stats_file.write(f"Processed files: {len(processed_files)}\n")
        stats_file.write(f"Total code lines: {total_code_lines:,}\n")
        stats_file.write(f"Total tokens: {total_tokens:,}\n")
        stats_file.write(f"Excluded files: {len(excluded_files)}\n\n")
        stats_file.write("File Types Distribution\n")
        stats_file.write("=====================\n")
        for ext, count in sorted(file_types.items()):
            if ext:
                percentage = (count / len(processed_files)) * 100
                stats_file.write(f"{ext}: {count:,} files ({percentage:.1f}%)\n")
            else:
                percentage = (count / len(processed_files)) * 100
                stats_file.write(f"No extension: {count:,} files ({percentage:.1f}%)\n")
        
        if excluded_files:
            stats_file.write("\nExcluded Files\n")
            stats_file.write("=============\n")
            for file in sorted(excluded_files):
                stats_file.write(f"- {file}\n")

if __name__ == "__main__":
    print("Welcome to the Project Structure and Code Extractor!")

    project_name = input("Enter the project name: ").strip()
    project_path = input("Enter the path to your project directory: ").strip()

    print(f"\nProcessing project '{project_name}' located at '{project_path}'...")

    # Generate directory mapping
    collect_directory_mapping(project_path)
    print("Directory mapping saved to 'directory.txt'.")

    # Generate file contents
    generate_file_contents(project_path)
    print("File contents saved to 'codebase.txt'.")

    # Generate statistics
    generate_stats('directory.txt', 'codebase.txt')
    print("Statistics saved to 'stats.txt'.")

    print("Process completed successfully!")

