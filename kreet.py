import random
import requests
import time
import imaplib
import email

# Set to store used numbers
used_numbers = set()
min_number = 500

# ZohoMail Credentials (Modify these)
ZOHO_IMAP_SERVER = "imap.zoho.com"
ZOHO_EMAIL = "ryliecohn@zohomail.com"  # Replace with your Zoho email
ZOHO_PASSWORD = "kirbsmaot321"  # Replace with your Zoho password

def generate_unique_number():
    """Generates a unique number ensuring no duplicates."""
    while True:
        random_number = random.randint(min_number, 1000000 + min_number)
        if random_number not in used_numbers:
            used_numbers.add(random_number)
            return random_number

def generate_email():
    """Generates a unique ZohoMail email address."""
    email_counter = generate_unique_number()
    email = f"ryliecohn+{email_counter}@zohomail.com"
    return email

def create_facebook_account(email, password):
    """Simulates Facebook account creation (replace with actual implementation)."""
    url = "https://m.facebook.com/reg"
    data = {
        "email": email,
        "password": password,
        "name": "John Doe",
        "birthdate": "01/01/2000",
        "gender": "male"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, data=data, headers=headers)
    
    # Simulated success check (modify based on actual response handling)
    if response.status_code == 200 and "checkpoint" not in response.text:
        return {"success": True, "fb_uid": "1234567890"}  # Replace with actual Facebook UID retrieval
    return {"success": False}

def check_zoho_for_otp(email_prefix):
    """Checks ZohoMail inbox for OTP related to the email."""
    try:
        mail = imaplib.IMAP4_SSL(ZOHO_IMAP_SERVER)
        mail.login(ZOHO_EMAIL, ZOHO_PASSWORD)
        
        # Check multiple folders (Inbox, Spam, Notifications)
        folders_to_check = ["Inbox", "Spam", "Notifications"]
        
        for folder in folders_to_check:
            mail.select(folder)
            print(f"🔍 Checking folder: {folder}...")

            # Search for emails containing the email prefix
            result, data = mail.search(None, 'ALL')
            mail_ids = data[0].split()

            for mail_id in reversed(mail_ids):  # Start from the latest email
                result, msg_data = mail.fetch(mail_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]

                        # Modify this to match FB OTP email format
                        if "Facebook Confirmation Code" in subject:
                            body = msg.get_payload(decode=True).decode("utf-8")
                            otp_code = extract_otp(body)  # Extract OTP from the email body
                            if otp_code:
                                return otp_code
        return None
    except Exception as e:
        print("❌ Error checking ZohoMail:", e)
        return None

def extract_otp(text):
    """Extracts OTP from email body."""
    import re
    match = re.search(r"\b\d{6}\b", text)  # Assuming OTP is a 6-digit code
    return match.group(0) if match else None

def save_email(email):
    """Saves the successfully used email to emails.txt."""
    with open("emails.txt", "a") as file:
        file.write(email + "\n")

def main():
    """Main function to generate and register Facebook accounts."""
    num_accounts = int(input("Enter the number of accounts to create: "))

    for _ in range(num_accounts):
        email = generate_email()
        password = "Random@1234"  # You can generate a random password instead

        print(f"🚀 Creating account with {email}...")
        fb_response = create_facebook_account(email, password)

        if fb_response["success"]:
            print(f"✅ Account created successfully with {email}")

            # Retry checking for OTP every 30 seconds for up to 5 minutes
            otp = None
            email_prefix = email.split("@")[0]  # Extract prefix for searching
            
            for attempt in range(10):  # 10 attempts (every 30 seconds for 5 minutes)
                print(f"🔄 Checking for OTP (Attempt {attempt + 1}/10)...")
                otp = check_zoho_for_otp(email_prefix)
                
                if otp:
                    break  # Exit loop if OTP is found
                
                time.sleep(30)  # Wait 30 seconds before retrying

            if otp:
                print("\n📩 **Facebook Account Details**")
                print(f"📧 Email: {email}")
                print(f"🔑 Password: {password}")
                print(f"🆔 Facebook UID: {fb_response['fb_uid']}")
                print(f"🔢 OTP: {otp}\n")

                save_email(email)  # Save only if OTP is found
            else:
                print(f"⚠️ No OTP found for {email}. Account may not be fully registered.")
        else:
            print(f"❌ Failed to create account with {email}, retrying...")
            time.sleep(2)  # Optional delay before retrying

if __name__ == "__main__":
    main()
