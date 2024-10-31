# Qodana SARIF Report Extraction Tool

This tool extracts and formats issues from Qodana SARIF reports into a user-friendly, language-model-compatible (LLM-friendly) summary. It prompts users for configuration, including file paths and details to include, making it simple and interactive.

## Features

- **User Prompts**: Asks for SARIF input file path, output file path, and code snippet inclusion.
- **LLM-Friendly Format**: Outputs a structured report for easy reading by language models and users.
- **Confirmation & Error Handling**: Confirms settings before running and checks for errors in the SARIF file.

## Usage

**Requires**:
   Script requires Python 3.6 or later.

run this in command

```bash
python qodana_extractor.py
```

### Example Run

```plaintext
Qodana SARIF Report Extraction Tool
Enter the path to the Qodana SARIF report (e.g., 'qodana_report.sarif.json'): qodana_report.sarif.json
Enter the desired output file path (e.g., 'llm_friendly_report.txt'): llm_friendly_report.txt
Would you like to include code snippets in the output? (y/n): y

--- Confirmation ---
SARIF File Path: qodana_report.sarif.json
Output File Path: llm_friendly_report.txt
Include Code Snippets: Yes
Proceed with these settings? (y/n): y

Loaded SARIF file from 'qodana_report.sarif.json'.
Extraction complete. LLM-friendly report saved to 'llm_friendly_report.txt'.
```

### Output Format

The extracted report contains a summary of issues in a format that includes:

- Rule ID
- Message describing the issue
- Severity level
- File locations with optional code snippets for easy reference

### Example Output

```plaintext
Issue with ruleId 'GO-001' (Level: warning):
- Message: Variable 'x' is unused
- Locations:
  * File: main.go at line 42
    Snippet: var x = 10
```

## Configuration

- **SARIF Path**: Path to the Qodana SARIF report file.
- **Output Path**: Desired output file path for the LLM-friendly report.
- **Include Snippets**: Option to include code snippets for each issue.
