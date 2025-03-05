import os
import re
import time
import html2text
import subprocess
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse


def download_gitbook(url, output_dir):
    print(f"Downloading GitBook from {url} to {output_dir}...")
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    wget_command = [
        "wget",
        "--mirror",
        "--convert-links",
        "--adjust-extension",
        "--page-requisites",
        "--no-parent",
        f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        f"--directory-prefix={output_dir}",
        url,
    ]
    try:
        subprocess.run(wget_command, check=True)
        print("Download completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading site: {e}")
        return False
    except FileNotFoundError:
        print(
            "Error: wget not found. Please install wget or make sure it's in your PATH."
        )
        return False


def fix_html_links(html_dir, domain):
    print("\nFixing HTML links to work locally...")
    fixed_files = 0
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    pattern = r'href="https?://' + re.escape(domain) + r'/(.*?)"'
                    replacement = r'href="\1"'
                    updated_content = re.sub(pattern, replacement, content)
                    if content != updated_content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(updated_content)
                        fixed_files += 1
                        print(f"Fixed links in {file_path}")
                except Exception as e:
                    print(f"Error fixing links in {file_path}: {str(e)}")

    print(f"Fixed links in {fixed_files} HTML files")
    return fixed_files


def html_to_markdown(html_content, domain):
    soup = BeautifulSoup(html_content, "html.parser")
    for img in soup.find_all("img"):
        img.decompose()
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_links = False
    h.body_width = 0
    markdown = h.handle(str(soup))
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = re.sub(r"\((.*?)\.html\)", r"(\1.md)", markdown)
    pattern = r"\(https?://" + re.escape(domain) + r"/(.*?)\.html(#[^)]+)?\)"
    replacement = r"(\1.md\2)"
    markdown = re.sub(pattern, replacement, markdown)
    return markdown


def process_directory(html_dir, output_dir, domain):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    total_files = 0
    processed_files = 0
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file.endswith(".html"):
                total_files += 1
    if total_files == 0:
        print("No HTML files found to process.")
        return 0
    print(f"Found {total_files} HTML files to process.")
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file.endswith(".html"):
                html_path = os.path.join(root, file)
                rel_path = os.path.relpath(html_path, html_dir)
                md_path = os.path.join(output_dir, rel_path.replace(".html", ".md"))
                Path(os.path.dirname(md_path)).mkdir(parents=True, exist_ok=True)
                try:
                    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                        html_content = f.read()
                    markdown_content = html_to_markdown(html_content, domain)
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(markdown_content)
                    processed_files += 1
                    print(
                        f"[{processed_files}/{total_files}] Converted {html_path} to {md_path}"
                    )
                except Exception as e:
                    print(f"Error processing {html_path}: {str(e)}")
    return processed_files


def fix_links_in_markdown_files(markdown_dir, domain):
    print("\nPerforming second pass to fix internal links...")
    fixed_files = 0
    for root, dirs, files in os.walk(markdown_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    updated_content = re.sub(
                        r"\((.*?)\.html(#[^)]+)?\)", r"(\1.md\2)", content
                    )
                    domain_pattern = (
                        r"\(https?://" + re.escape(domain) + r"/(.*?)\.html(#[^)]+)?\)"
                    )
                    updated_content = re.sub(
                        domain_pattern, r"(\1.md\2)", updated_content
                    )
                    if content != updated_content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(updated_content)
                        fixed_files += 1
                        print(f"Fixed links in {file_path}")
                except Exception as e:
                    print(f"Error fixing links in {file_path}: {str(e)}")
    print(f"Fixed links in {fixed_files} files")
    return fixed_files


def main():
    print("GitBook Downloader and Converter")
    print("------------------------------------------")
    try:
        try:
            subprocess.run(
                ["wget", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except FileNotFoundError:
            print("Error: wget is not installed or not in PATH.")
            print("Please install wget first to download GitBook content.")
            input("Press Enter to exit...")
            sys.exit(1)
        gitbook_url = input("Enter the GitBook URL to download: ")
        if not gitbook_url:
            print("Error: URL cannot be empty.")
            input("Press Enter to exit...")
            sys.exit(1)
        if not gitbook_url.startswith(("http://", "https://")):
            gitbook_url = "https://" + gitbook_url
            print(f"Added protocol: {gitbook_url}")
        parsed_url = urlparse(gitbook_url)
        domain = parsed_url.netloc
        base_name = domain.split(".")[0]
        default_html_dir = f"./{base_name}_html"
        default_md_dir = f"./{base_name}_markdown"
        html_dir = input(
            f"Enter directory to save downloaded HTML [default: {default_html_dir}]: "
        )
        if not html_dir:
            html_dir = default_html_dir
        md_dir = input(
            f"Enter directory to save converted Markdown [default: {default_md_dir}]: "
        )
        if not md_dir:
            md_dir = default_md_dir
        download_new = input("\nDownload new content? (y/n): ").lower() == "y"
        start_time = time.time()
        if download_new:
            success = download_gitbook(gitbook_url, html_dir)
            if not success:
                print("Download failed. Exiting.")
                input("Press Enter to exit...")
                sys.exit(1)
            fix_html_links(html_dir, domain)
        else:
            if not os.path.isdir(html_dir):
                print(f"Error: HTML directory '{html_dir}' does not exist.")
                input("Press Enter to exit...")
                sys.exit(1)
        convert_to_md = input("\nConvert to Markdown? (y/n): ").lower() == "y"
        processed_count = 0
        fixed_count = 0
        if convert_to_md:
            print("\nStarting conversion to Markdown...\n")
            processed_count = process_directory(html_dir, md_dir, domain)
            if processed_count > 0:
                fixed_count = fix_links_in_markdown_files(md_dir, domain)
        end_time = time.time()
        duration = end_time - start_time
        print("\nProcess complete!")
        if download_new:
            print(f"Downloaded GitBook from {gitbook_url}")
        if convert_to_md and processed_count > 0:
            print(f"Processed {processed_count} HTML files in {duration:.2f} seconds")
            print(f"Fixed links in {fixed_count} markdown files")
            print(f"HTML files are saved in: {os.path.abspath(html_dir)}")
            print(f"Markdown files are saved in: {os.path.abspath(md_dir)}")
        else:
            print(f"HTML files are saved and fixed in: {os.path.abspath(html_dir)}")
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
        input("Press Enter to exit...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
