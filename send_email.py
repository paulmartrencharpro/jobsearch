import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(content):
    sender_email = "bot.martrenchar@gmail.com"
    receiver_email = "paul.martrenchar@gmail.com"
    password = os.environ.get('GMAIL_PASSWORD')

    message = MIMEMultipart("related")
    message["Subject"] = "Job offers"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(content, "html"))

    # Create secure connection with server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Enable security
        server.starttls()
        
        # Login to the server
        server.login(sender_email, password)
        
        # Send email
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        print("Email sent")