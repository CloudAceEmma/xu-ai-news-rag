import feedparser
import requests
from bs4 import BeautifulSoup
from backend.models import db, User, RssFeed
from backend.services.knowledge_base import add_document_to_kb
from backend.services.notification import send_notification
import os
from werkzeug.utils import secure_filename

def get_article_content(url):
    """Fetches and extracts the main content of an article."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # A simple approach to get text; can be improved with more advanced extraction
        paragraphs = soup.find_all('p')
        return "\n".join([p.get_text() for p in paragraphs])
    except requests.RequestException as e:
        print(f"Error fetching article content from {url}: {e}")
        return None

def run_aggregation_for_all_users(app):
    """
    Fetches and processes articles from all RSS feeds for all users.
    """
    with app.app_context():
        users = User.query.all()
        for user in users:
            feeds = RssFeed.query.filter_by(user_id=user.id).all()
            for feed in feeds:
                d = feedparser.parse(feed.url)
                for entry in d.entries:
                    content = get_article_content(entry.link)
                    if content:
                        # Save content to a temporary file
                        temp_dir = "temp_articles"
                        os.makedirs(temp_dir, exist_ok=True)
                        file_path = os.path.join(temp_dir, f"{user.id}_{secure_filename(entry.link)}.txt")
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        
                        # Add the document to the knowledge base
                        add_document_to_kb(
                            file_path=file_path,
                            document_type='txt',
                            source=entry.link,
                            tags=','.join(tag.term for tag in entry.tags) if hasattr(entry, 'tags') else None
                        )
                        
                        # Send notification
                        send_notification(
                            subject="New Document Added to Knowledge Base",
                            recipients=[app.config['ADMIN_EMAIL']],
                            body=f"A new document from {entry.link} has been added for user {user.username}."
                        )
