import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, body, receiver_email=None):
    sender_email = os.getenv("GMAIL_USER")
    sender_password = os.getenv("GMAIL_APP_PASSWORD") # Recommended to use App Password
    
    if not sender_email or not sender_password:
        print("Error: GMAIL_USER or GMAIL_APP_PASSWORD not set in .env")
        return False

    if not receiver_email:
        receiver_email = sender_email

    # Create Message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent successfully to {receiver_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    # Test execution if running directly
    report_path = "reddit_news_report.txt"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            content = f.read()
        send_email("Reddit Signal Report", content)
    else:
        print("Report file not found for testing.")
