import requests
import random
import string
import time
from termcolor import colored

# Generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Fetch a working proxy from multiple sources
def get_proxy():
    proxy_sources = [
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ]
    
    for url in proxy_sources:
        try:
            response = requests.get(url, timeout=5)
            print(colored(f"[DEBUG] Proxy API Response ({url}):\n", "cyan"), response.text[:200])  # Show first 200 chars
            
            proxies = response.text.splitlines()
            if proxies:
                return random.choice(proxies)
        except requests.exceptions.RequestException:
            continue
    return None

# Get a temporary email from multiple sources
def get_temp_email():
    email_sources = [
        "https://www.1secmail.net/api/v1/?action=genRandomMailbox",
        "https://api.mail.tm/domains"
    ]
    
    for url in email_sources:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            print(colored(f"[DEBUG] Email API Response ({url}):\n", "cyan"), response.text[:200])  # Show first 200 chars
            
            if response.status_code == 200:
                data = response.json()
                
                if "1secmail" in url:
                    return data[0] if isinstance(data, list) else None
                
                elif "mail.tm" in url and "hydra:member" in data:
                    domains = data["hydra:member"]
                    if domains:  # Ensure list is not empty
                        return f"fbuser{random.randint(1000,9999)}@{domains[0]['id']}"
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            print(colored(f"[ERROR] Failed to fetch email from {url}. Retrying...", "red"))
            continue
    
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
