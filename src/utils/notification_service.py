# notification_service.py
import smtplib
from email.mime.text import MIMEText

class NotificationService:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_email: str, subject: str, message: str):
        """Send an email notification."""
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to_email, msg.as_string())

    def notify_transaction_status(self, to_email: str, transaction_id: str, status: str):
        """Notify user about the transaction status."""
        subject = f"Transaction Status Update: {transaction_id}"
        message = f"Your transaction with ID {transaction_id} has been {status}."
        self.send_email(to_email, subject, message)
