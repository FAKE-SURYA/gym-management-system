import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings

settings = get_settings()


def send_email(to: str, subject: str, body: str) -> bool:
    """Send email using SMTP"""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("Email credentials not configured")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent to {to}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
