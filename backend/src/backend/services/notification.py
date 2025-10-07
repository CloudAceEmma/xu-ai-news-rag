from flask_mail import Message
from backend.app import mail

def send_notification(subject, recipients, body):
    """Sends an email notification."""
    msg = Message(subject, recipients=recipients)
    msg.body = body
    try:
        mail.send(msg)
    except Exception as e:
        # In a real app, you'd want to log this error.
        print(f"Error sending email: {e}")
