from unittest.mock import patch
from backend.services.notification import send_notification
from flask_mail import Message

def test_send_notification(app):
    """Test that the send_notification function constructs and sends an email."""
    with app.app_context():
        with patch('backend.app.mail.send') as mock_send:
            subject = "Test Subject"
            recipients = ["test@example.com"]
            body = "This is a test body."
            
            send_notification(subject, recipients, body)
            
            mock_send.assert_called_once()
            args, _ = mock_send.call_args
            sent_message = args[0]
            
            assert isinstance(sent_message, Message)
            assert sent_message.subject == subject
            assert sent_message.recipients == recipients
            assert sent_message.body == body
