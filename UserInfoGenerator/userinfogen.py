import random
import string
from datetime import datetime, timedelta
import subprocess
import sys
import os

def check_and_install_names():
    try:
        import names
        return True
    except ImportError:
        print("\nThe 'names' module is required but not installed.")
        choice = input("Would you like to install it:\n1. Globally (default Python installation)\n2. In a virtual environment in the current directory\n\nEnter your choice (1/2): ")
        
        if choice == "2":
            venv_path = os.path.join(os.getcwd(), "venv")
            if not os.path.exists(venv_path):
                subprocess.run([sys.executable, "-m", "venv", venv_path])
            
            if os.name == "nt":
                pip_path = os.path.join(venv_path, "Scripts", "pip")
            else:
                pip_path = os.path.join(venv_path, "bin", "pip")
                
            subprocess.run([pip_path, "install", "names"])
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", "names"])
        
        return True

def generate_username(first_name, last_name):
    patterns = [
        f"{first_name.lower()}{last_name.lower()[:2]}",
        f"{first_name[0].lower()}{last_name.lower()}",
        f"{last_name.lower()}{random.randint(10,99)}"
    ]
    return random.choice(patterns)

def generate_password():
    length = random.randint(10, 16)
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

def generate_dob():
    start_date = datetime(1960, 1, 1)
    end_date = datetime(2005, 12, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%m/%d/%Y")

def generate_user_data(num_records=10):
    import names
    with open("user_data.txt", "w") as file:
        for _ in range(num_records):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            username = generate_username(first_name, last_name)
            password = generate_password()
            dob = generate_dob()
            
            user_data = (
                f"Username: {username}\n"
                f"Password: {password}\n"
                f"First Name: {first_name}\n"
                f"Last Name: {last_name}\n"
                f"DOB: {dob}\n"
                f"{'='*40}\n"
            )
            file.write(user_data)

if __name__ == "__main__":
    if check_and_install_names():
        try:
            num_records = int(input("How many records would you like to generate? "))
            generate_user_data(num_records)
            print(f"Generated {num_records} records in user_data.txt")
        except ValueError:
            print("Please enter a valid number.")