# === main.py ===

from ip_locator import get_ip_location
from phone_locator import get_phone_info
from email_locator import get_email_location, extract_sender_ip
import logging

# === Setup logging ===
logging.basicConfig(filename="bot_log.txt", level=logging.INFO)

def log_info(message):
    logging.info(message)

def log_error(error):
    logging.error(error)

# === IP Processing ===
def process_ip(ip_address):
    try:
        print("\n🔍 Processing IP Location...")
        get_ip_location(ip_address)
        log_info(f"Processed IP location for {ip_address}")
    except Exception as e:
        log_error(f"Error processing IP {ip_address}: {e}")
        print(f"❌ Error processing IP {ip_address}: {e}")

# === Phone Processing ===
def process_phone_number(phone_number):
    try:
        print("\n📱 Processing Phone Number Location...")
        get_phone_info(phone_number)
        log_info(f"Processed phone number location for {phone_number}")
    except Exception as e:
        log_error(f"Error processing phone number {phone_number}: {e}")
        print(f"❌ Error processing phone number {phone_number}: {e}")

# === Email Processing ===
def process_email(email_header):
    try:
        print("\n✉️ Processing Email Header...")
        ip_address = extract_sender_ip(email_header)
        if ip_address:
            get_email_location(ip_address)
            log_info(f"Processed email location for IP {ip_address}")
        else:
            print("⚠️ No IP address found in email headers.")
            log_info("No IP address found in email headers.")
    except Exception as e:
        log_error(f"Error processing email: {e}")
        print(f"❌ Error processing email: {e}")

# === User Interface ===
def get_user_input():
    try:
        print("\n=== Location Detection Menu ===")
        print("1) IP Address")
        print("2) Phone Number")
        print("3) Email Header")
        choice = input("Select input type (1/2/3): ")

        if choice == '1':
            ip = input("Enter IP address: ")
            process_ip(ip)
        elif choice == '2':
            phone = input("Enter phone number (with country code, e.g. +91...): ")
            process_phone_number(phone)
        elif choice == '3':
            headers = input("Paste email header: ")
            process_email(headers)
        else:
            print("❌ Invalid choice. Please choose 1, 2, or 3.")
    except Exception as e:
        log_error(f"Error in user input: {e}")
        print(f"❌ Input error: {e}")

# === Main Loop ===
def main():
    print("🤖 Welcome to the Location Detection Bot!")
    while True:
        get_user_input()
        again = input("\nDo you want to run another check? (y/n): ").lower()
        if again != 'y':
            print("👋 Exiting... Stay safe!")
            break

# === Entry Point ===
if __name__ == "__main__":
    main()
