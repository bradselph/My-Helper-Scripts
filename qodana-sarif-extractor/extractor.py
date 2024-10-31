import json
import os

def extract_qodana_issues(sarif_path, output_path, include_snippet=True):
    # Load SARIF file
    try:
        with open(sarif_path, 'r') as sarif_file:
            sarif_data = json.load(sarif_file)
        print(f"Loaded SARIF file from '{sarif_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{sarif_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: File '{sarif_path}' is not a valid JSON file.")
        return

    issues = []

    for run in sarif_data.get('runs', []):
        for result in run.get('results', []):
            issue = {
                "ruleId": result.get("ruleId"),
                "message": result.get("message", {}).get("text"),
                "level": result.get("level"),
                "locations": []
            }
            
            for location in result.get("locations", []):
                location_info = location.get("physicalLocation", {})
                issue_location = {
                    "file": location_info.get("artifactLocation", {}).get("uri"),
                    "line": location_info.get("region", {}).get("startLine")
                }
                if include_snippet:
                    issue_location["snippet"] = location_info.get("region", {}).get("snippet", {}).get("text")
                issue["locations"].append(issue_location)
            
            issues.append(issue)

    llm_friendly_issues = []
    for issue in issues:
        llm_friendly_issue = (
            f"Issue with ruleId '{issue['ruleId']}' (Level: {issue['level']}):\n"
            f"- Message: {issue['message']}\n"
            f"- Locations:\n"
        )
        for loc in issue["locations"]:
            location_str = f"  * File: {loc['file']} at line {loc['line']}\n"
            if include_snippet and "snippet" in loc:
                location_str += f"    Snippet: {loc['snippet']}\n"
            llm_friendly_issue += location_str
        llm_friendly_issues.append(llm_friendly_issue)

    # Save to output file
    with open(output_path, 'w') as output_file:
        output_file.write("\n\n".join(llm_friendly_issues))
    print(f"Extraction complete. LLM-friendly report saved to '{output_path}'.")

# User Input for Paths and Options
def main():
    print("Qodana SARIF Report Extraction Tool")
    
    # Input SARIF file path
    sarif_path = input("Enter the path to the Qodana SARIF report (e.g., 'qodana_report.sarif.json'): ").strip()
    
    # Output file path
    output_path = input("Enter the desired output file path (e.g., 'llm_friendly_report.txt'): ").strip()

    # Option to include code snippet
    include_snippet = input("Would you like to include code snippets in the output? (y/n): ").strip().lower() == 'y'
    
    # Confirm details
    print("\n--- Confirmation ---")
    print(f"SARIF File Path: {sarif_path}")
    print(f"Output File Path: {output_path}")
    print(f"Include Code Snippets: {'Yes' if include_snippet else 'No'}")
    
    confirm = input("Proceed with these settings? (y/n): ").strip().lower()
    if confirm == 'y':
        extract_qodana_issues(sarif_path, output_path, include_snippet)
    else:
        print("Operation canceled.")

if __name__ == "__main__":
    main()
