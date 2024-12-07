import imaplib
import email
import webbrowser
import schedule 
import os
import re
import time
from plyer import notification
from dotenv import load_dotenv
from email.header import decode_header
from win10toast_click import ToastNotifier

load_dotenv()


def load_processed_ids(log_file="processed_ids.log"):
    """Load processed message IDs from a log file."""
    if not os.path.exists(log_file):
        return set()
    with open(log_file, "r") as file:
        return set(line.strip() for line in file)

def save_processed_id(msg_id, log_file="processed_ids.log"):
    """Save a processed message ID to the log file."""
    with open(log_file, "a") as file:
        file.write(f"{msg_id}\n")

def decode_value(value):
    """Decode email headers (like subject or sender)."""
    decoded = decode_header(value)
    value_part = decoded[0][0]
    encoding = decoded[0][1]
    if isinstance(value_part, bytes):
        return value_part.decode(encoding or "utf-8")
    return value_part

def extract_email(from_field):
    """Extract only the email address from the From field."""
    match = re.search(r'<(.*?)>', from_field)  # Matches the email address inside <>
    return match.group(1) if match else from_field  # Return the email or the whole field if no match

def send_notification(new_emails):
    """Send a desktop notification summarizing new emails and open Gmail on click."""
    try:
            toaster = ToastNotifier()
            count = len(new_emails)
            
            if count == 1:
                sender_email, subject = new_emails[0]
                toaster.show_toast(
                    "New Email Notification",
                    f"From: {sender_email}\nSubject: {subject}",
                    duration=15,
                    threaded=True,
                    callback_on_click=lambda: webbrowser.open("https://mail.google.com/")
                )
            elif count > 1:
                toaster.show_toast(
                    "New Email Notification",
                    f"You have {count} new emails.",
                    duration=15,
                    threaded=True,
                    callback_on_click=lambda: webbrowser.open("https://mail.google.com/")
                )
    except Exception as e:
            print(f"Notification Error: {e}")
        


def check_gmail():
    # Gmail IMAP server details
    imap_server=os.environ.get('IMAP_SERVER')
    email_user = os.environ.get('EMAIL_USER') # Your email address
    email_pass=os.environ.get('EMAIL_PASS') # Your email password

 # Load already processed message IDs
    processed_ids = load_processed_ids()

    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)

        # Select the inbox
        mail.select("inbox")

        # Search for unread emails
        status, messages = mail.search(None, '(UNSEEN)')
        if status != "OK" or not messages[0]:
            print("No new messages found!")
            return

        # Collect new emails for notification
        new_emails = []

        for num in messages[0].split():
            if num in processed_ids:
                continue  # Skip already processed emails

            # Fetch the email by ID
            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                print(f"Failed to fetch message ID {num}.")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse the raw email
                    msg = email.message_from_bytes(response_part[1])
                    # Decode the email subject
                    subject = decode_value(msg["Subject"])

                    # Decode the sender and extract email address
                    from_ = decode_value(msg.get("From", "Unknown Sender"))
                    sender_email = extract_email(from_)

                    # Log and collect the email
                    print(f"New Email:\n  From: {sender_email}\n  Subject: {subject}\n")
                    new_emails.append((sender_email, subject))
                    save_processed_id(num)

        # Send a notification summarizing new emails
        send_notification(new_emails)

        # Close the connection and logout
        mail.close()
        mail.logout()

    except Exception as e:
        print(f"An error occurred: {e}")
        
        
# Schedule the task every 10 minute
schedule.every(10).minutes.do(check_gmail)

if __name__ == "__main__":
    # Run the email check periodically
    while True:
        print("Checking for new emails...")
        check_gmail()
        print("Waiting for 1 minutes before re-checking...")
        time.sleep(510)  # Wait for 510 seconds (8.5 minutes) before re-checking