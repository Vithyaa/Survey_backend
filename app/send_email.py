import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

def send_email_with_attachment(to_email: str, attachment: bytes):

    # Set up the message
    subject = "Survey Registration"
    body = f"Thank you for partcipate our Survey!\n\nRegards:\nSurvey Team"

    # Create a MIMEMultipart object
    message = MIMEMultipart()
    message["From"] = os.getenv("SMTP_USER")
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach the PDF
    pdf_attachment = MIMEApplication(attachment, _subtype='pdf')
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename='output.pdf')
    message.attach(pdf_attachment)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT")) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_USER"), to_email, message.as_string())

