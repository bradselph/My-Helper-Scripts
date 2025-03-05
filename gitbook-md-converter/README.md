# GitBook to Markdown Converter

A Python script that downloads GitBook documentation sites and optionally converts them to clean Markdown files with working internal links.

## Features

- Downloads complete GitBook documentation sites using wget
- Optionally converts HTML pages to clean Markdown format
- Fixes HTML links to work locally, even without conversion
- Strips images while preserving text content and structure when converting
- Fixes internal links between Markdown files
- Works with any GitBook site

## Requirements

- Python 3.6 or higher
- wget command-line tool
- Python packages:
  - beautifulsoup4
  - html2text

## Installation

1. Clone this repository:
   ```cmd
   git clone https://github.com/bradselph/My-Helper-Scripts.git
   cd My-Helper-Scripts/gitbook-md-converter
   ```

2. Install required Python packages:
   ```
   pip install beautifulsoup4 html2text
   ```

3. Ensure wget is installed on your system:
   - **Windows**: Install via [Chocolatey](https://chocolatey.org/): `choco install wget` or [Scoop](https://scoop.sh/): `scoop install wget`
   - **macOS**: Install via [Homebrew](https://brew.sh/): `brew install wget`
   - **Linux**: Should be included by default, or install via your package manager: `apt install wget` or `yum install wget`

## Usage

1. Run the script:
   ```cmd
   python gitbook_to_markdown.py
   ```

2. Follow the interactive prompts:
   - Enter the GitBook URL you want to download
   - Specify directories for HTML and Markdown files (or accept defaults)
   - Choose whether to download new content or use existing files
   - Select whether to convert HTML to Markdown or just fix HTML links

3. The script will:
   - Download the GitBook site (if requested)
   - Fix HTML links to work locally
   - Convert to Markdown if selected
   - Create a browsable version of the documentation


## Example

```cmd
GitBook Downloader and Converter
------------------------------------------
Enter the GitBook URL to download: https://docs.example.com/
Enter directory to save downloaded HTML [default: ./example_html]:
Enter directory to save converted Markdown [default: ./example_markdown]:

Download new content? (y/n): y
Downloading GitBook from https://docs.example.com/ to ./example_html...
Download completed successfully

Convert to Markdown? (y/n): y
Starting conversion to Markdown...
Found 35 HTML files to process.
[1/35] Converted ./example_html/docs.example.com/index.html to ./example_markdown/docs.example.com/index.md

Performing second pass to fix internal links...
Fixed links in 32 files
Process complete!

Downloaded GitBook from https://docs.example.com/
Processed 35 HTML files in 10.22 seconds
Fixed links in 32 files
HTML files are saved in: /path/to/example_html
Markdown files are saved in: /path/to/example_markdown

Press Enter to exit...
```

GitBook sites can be difficult to download with standard web scrapers because they:
- Use client-side JavaScript for rendering content
- Have complex URL structures for resources
- Often use dynamic loading for content

This script solves these issues by:
1. Using wget's advanced features to properly mirror the site
2. Fixing HTML links to work locally
3. Optionally converting to clean Markdown format
4. Fixing all internal links to work properly in the converted files

The result is a local, browsable copy of the documentation that works well with standard browsers or Markdown editors.