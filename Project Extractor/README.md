### README.md (Updated)

# Project Structure and Code Extractor

This Python script automates the process of extracting directory structures, file contents, and generating statistics for a given project. It utilizes the `tiktoken` library to tokenize code and calculates statistics such as the total number of files, folders, lines of code, and tokens in the project.

## Features
- **Directory Mapping**: Generates a tree-like structure of the project and saves it to `directory.txt`.
- **File Content Extraction**: Reads and saves the contents of all files (excluding binaries and images) to `contents.txt` in an XML-like format.
- **Statistics Generation**: Provides a summary of the project, including the number of files, folders, lines of code, and tokens in `stats.txt`.

## Installation
Before running the script, ensure that you have the `tiktoken` library installed. The script will attempt to install the library automatically if it's not present.

```bash
pip install tiktoken
```

Alternatively, run the script, and it will handle the installation for you.

## Usage
Run the script in the terminal and follow the prompts to enter your project name and path:

```bash
python script_name.py
```

The script will generate three files:
- **`directory.txt`**: The structure of the project directory.
- **`contents.txt`**: The extracted contents of all files (in an XML-like format).
- **`stats.txt`**: Statistics about the project (total files, folders, lines of code, and tokens).

## Exclusions
The following file types and directories are excluded from content extraction:
- **File extensions**: `.exe`, `.dll`, `.bin`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.ico`, `.svg`
- **Directories**: `.git`, `.github`, `.idea`

## License
This project is licensed under the **GNU Affero General Public License v3.0**. See the [LICENSE](LICENSE) file for details.