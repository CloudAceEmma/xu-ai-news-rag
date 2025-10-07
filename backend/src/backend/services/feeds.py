from backend.models import db, RssFeed

def add_rss_feed(user_id, url):
    """Adds a new RSS feed for a user."""
    feed = RssFeed(user_id=user_id, url=url)
    db.session.add(feed)
    db.session.commit()
    return feed

def get_user_feeds(user_id):
    """Retrieves all RSS feeds for a user."""
    return RssFeed.query.filter_by(user_id=user_id).all()

def delete_rss_feed(user_id, feed_id):
    """Deletes an RSS feed for a user."""
    feed = RssFeed.query.filter_by(id=feed_id, user_id=user_id).first()
    if feed:
        db.session.delete(feed)
        db.session.commit()
        return True
    return False
