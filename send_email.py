import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(subject, content):
    sender_email = os.environ.get('EMAIL_SENDER')
    password = os.environ.get('GMAIL_PASSWORD')
    receivers_email = [os.environ.get('EMAIL_1'), os.environ.get('EMAIL_2')]
    message = MIMEMultipart("related")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ", ".join(receivers_email)

    message.attach(MIMEText(content, "html"))

    # Create secure connection with server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Enable security
        server.starttls()
        
        # Login to the server
        server.login(sender_email, password)
        
        # Send email
        server.sendmail(
            sender_email, receivers_email, message.as_string()
        )
        print("Email sent")