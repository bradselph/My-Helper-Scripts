import re
import os

def extract_provider(email):
    # Extract the domain part of the email (provider)
    return email.split('@')[-1]

def sort_emails(email_list):
    # Split email list into lines
    email_pairs = email_list.strip().split('\n')
    
    # Parse email and password pairs
    parsed_pairs = [line.split(':') for line in email_pairs]
    
    # Sort pairs by email provider and then by email address
    sorted_pairs = sorted(parsed_pairs, key=lambda pair: (extract_provider(pair[0]), pair[0]))
    
    # Rejoin sorted pairs into the desired format
    sorted_email_list = '\n'.join(f'{email}:{password}' for email, password in sorted_pairs)
    return sorted_email_list

def main():
    # Ask user for file path
    file_path = input("Enter the path to the file containing email-password pairs: ").strip()
    
    if not os.path.isfile(file_path):
        print("The file does not exist. Please check the path and try again.")
        return
    
    # Read the email-password pairs from the file
    with open(file_path, 'r') as file:
        email_list = file.read()
    
    # Count total emails
    total_emails = len(email_list.strip().split('\n'))
    
    # Sort emails
    sorted_email_list = sort_emails(email_list)
    
    # Write the sorted list to a new file
    sorted_file_path = file_path.replace('.txt', '_sorted.txt')
    with open(sorted_file_path, 'w') as file:
        file.write(sorted_email_list)
    
    # Count sorted emails by provider
    sorted_email_pairs = sorted_email_list.strip().split('\n')
    provider_count = {}
    for line in sorted_email_pairs:
        email = line.split(':')[0]
        provider = extract_provider(email)
        if provider not in provider_count:
            provider_count[provider] = 0
        provider_count[provider] += 1
    
    print(f"Total emails found: {total_emails}")
    for provider, count in provider_count.items():
        print(f"Emails sorted by provider '{provider}': {count}")
    
    print(f"Sorted email-password pairs have been saved to {sorted_file_path}.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
