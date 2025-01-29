# Project Structure and Code Extractor

This Python script automates the process of extracting directory structures, file contents, and generating detailed statistics for a given project. It utilizes the `tiktoken` library for token counting and provides comprehensive project analysis.

## Features
- **Directory Mapping**: Generates a tree-like structure of the project directory and saves it to `directory.txt`
- **File Content Extraction**: Reads and saves the contents of all files (excluding binaries and images) to `codebase.txt` in an XML-like format
- **Project Statistics**: Generates detailed project statistics including file counts, code lines, tokens, and file type distribution in `stats.txt`
- **Progress Tracking**: Shows real-time progress during file processing
- **Automatic Dependency Installation**: Automatically installs required packages if not present

## Requirements
The script will automatically install required packages:
- `tiktoken`: For token counting
- `tqdm`: For progress tracking

## Usage
Run the script in your terminal:

```bash
python ProExtractor1.5.py
```

Follow the prompts to enter:
1. Project name
2. Project directory path

The script will generate three files:
- `directory.txt`: Complete directory structure
- `codebase.txt`: Extracted file contents in XML format
- `stats.txt`: Detailed project statistics

## Excluded Content
### File Extensions
```
.exe, .dll, .bin, .jpg, .jpeg, .png, .gif, .bmp, .ico, .svg, .pyc, .pyo
```

### Directories
```
.git, .github, .idea, __pycache__, node_modules, venv, env
```

## Output Format Examples

### directory.txt
```
├── src/
│   ├── main.py
│   ├── utils/
│   │   ├── helper.py
```

### codebase.txt
```xml
<file path='src/main.py'>
[file contents here]
</file>
```

### stats.txt
```
Project Statistics
=================

Total files: 100
Total folders: 15
Total code lines: 5000
Total tokens: 25000
Files ignored: 5

File Types Distribution
=====================
.py: 45 files
.js: 30 files
.css: 25 files

Ignored Files
============
- image.png
- binary.exe
```