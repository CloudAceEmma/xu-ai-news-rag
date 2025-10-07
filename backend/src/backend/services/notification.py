from flask_mail import Message
from backend.app import mail
import logging

def send_notification(subject, recipients, body):
    """Sends an email notification."""
    msg = Message(subject, recipients=recipients)
    msg.body = body
    try:
        mail.send(msg)
    except Exception as e:
        logging.error(f"Error sending email: {e}")
