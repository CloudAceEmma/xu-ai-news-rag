from unittest.mock import patch, MagicMock
from backend.services.aggregation import run_aggregation_for_all_users
from backend.models import db, User, RssFeed

def test_run_aggregation(app):
    """Test the aggregation service, mocking external calls."""
    with app.app_context():
        # Setup a user and a feed
        user = User(username="agg_user")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        feed_url = "file://" + os.path.abspath("tests/testdata/rss.xml")
        feed = RssFeed(user_id=user.id, url=feed_url)
        db.session.add(feed)
        db.session.commit()

    # Mock the services called by the aggregation function
    with patch('backend.services.aggregation.get_article_content') as mock_get_content, \
         patch('backend.services.aggregation.add_document_to_kb') as mock_add_doc, \
         patch('backend.services.aggregation.send_notification') as mock_send_notification:
        
        mock_get_content.return_value = "This is the article content."
        
        run_aggregation_for_all_users(app)

        # Assert that the mocks were called
        assert mock_get_content.call_count > 0
        assert mock_add_doc.call_count > 0
        assert mock_send_notification.call_count > 0
import os
