import requests
import random
import string
import time
import json
from termcolor import colored

# Generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Fetch a proxy
def get_proxy():
    response = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all")
    proxies = response.text.splitlines()
    return random.choice(proxies) if proxies else None

# Get a temporary email
def get_temp_email():
    response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox")
    if response.status_code == 200:
        return response.json()[0]
    return None

# Create a Facebook account
def create_fb_account():
    proxy = get_proxy()
    email = get_temp_email()
    password = generate_password()

    if not email or not proxy:
        print(colored("[ERROR] Failed to fetch email or proxy. Retrying...", "red"))
        return create_fb_account()

    print(colored(f"[+] Using Proxy: {proxy}", "cyan"))
    print(colored(f"[+] Email: {email}", "green"))
    print(colored(f"[+] Password: {password}", "yellow"))

    # Simulate account creation (Replace with actual Facebook signup request)
    success = random.choice([True, False])  # Simulated success/failure

    if success:
        print(colored("[✓] Account Created Successfully!", "green"))
        with open("accounts.txt", "a") as f:
            f.write(f"{email} | {password}\n")
    else:
        print(colored("[X] Failed to Create Account. Retrying...", "red"))
        return create_fb_account()

# Main menu
def menu():
    while True:
        print(colored("\nFB Auto Create - Developed by RYLE", "blue"))
        print(colored("1. Create Facebook Account", "green"))
        print(colored("2. View Created Accounts", "yellow"))
        print(colored("3. Exit", "red"))
        choice = input(colored("Select an option: ", "cyan"))

        if choice == "1":
            create_fb_account()
        elif choice == "2":
            with open("accounts.txt", "r") as f:
                print(f.read())
        elif choice == "3":
            print(colored("Exiting...", "red"))
            break
        else:
            print(colored("Invalid choice. Try again.", "red"))

if __name__ == "__main__":
    menu()
