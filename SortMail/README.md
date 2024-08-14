# Email Password Sorter

## Description

The **Email Password Sorter** is a Python script that reads a file containing email-password pairs, sorts the pairs by email provider and then by email address, and saves the sorted pairs to a new file. It also provides a summary of the total number of emails and a count of emails sorted by each provider.

## Features

- **Provider Extraction:** Extracts the domain part of the email (provider) for sorting purposes.
- **Sorting:** Sorts email-password pairs first by email provider and then by email address.
- **File Handling:** Reads from an input file and writes the sorted pairs to a new file.
- **Provider Count:** Counts the number of email-password pairs for each provider and displays the results.
- **User Interaction:** Prompts the user for the file path, handles file operations, and provides informative output.

## How It Works

1. **File Path Input:** The script prompts the user to enter the path to a file containing email-password pairs in the format `email:password`.
2. **File Validation:** Checks if the specified file exists. If not, it notifies the user and exits.
3. **Email Extraction:** Reads the email-password pairs from the file and extracts the email providers.
4. **Sorting:** Sorts the pairs by email provider and email address.
5. **Saving Results:** Saves the sorted pairs to a new file with `_sorted` appended to the original filename.
6. **Provider Count:** Counts and displays the number of email-password pairs for each provider.
7. **User Notification:** Provides a summary of the total emails and counts by provider, and waits for user input to exit.

## Usage

1. **Save the Script:** Copy the script into a file named `email_password_sorter.py`.
2. **Run the Script:** Open a terminal or command prompt and navigate to the directory where the script is saved. Run the script using:
   ```bash
   python email_password_sorter.py
   ```
3. **Provide File Path:** When prompted, enter the path to the text file containing email-password pairs.
4. **Review Results:** The script will display the total number of emails, count emails by provider, and save the sorted pairs to a new file.

## Example

Given an input file `emails.txt` with the following content:

```
john.doe@gmail.com:password123
jane.smith@yahoo.com:password456
alice@example.com:password789
```

The script will generate a file `emails_sorted.txt` with content sorted by provider:

```
alice@example.com:password789
john.doe@gmail.com:password123
jane.smith@yahoo.com:password456
```

And it will output:

```
Total emails found: 3
Emails sorted by provider 'example.com': 1
Emails sorted by provider 'gmail.com': 1
Emails sorted by provider 'yahoo.com': 1
Sorted email-password pairs have been saved to emails_sorted.txt.
```

## Notes

- Ensure that the input file is a plain text file with email-password pairs formatted as `email:password`.
- The script assumes that the email addresses are well-formed and that there are no duplicate entries.
