import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
def send_email(s_mail,r_mail):
    sender_email = s_mail
    receiver_email = r_mail
    subject = "Subject of the Email"
    message = "Body of the email goes here."

    # Gmail SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Port for TLS encryption

    # Login credentials (generally, you should use environment variables or a secure method to store these)
    smtp_username = "your.email@gmail.com"
    smtp_password = "your-gmail-password"  # If you're using 2-factor authentication, use an App Password here

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish a secure session with Gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure (TLS) mode
        server.login(smtp_username, smtp_password)  # Login with your Gmail address and App Password

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the server connection
        server.quit()
