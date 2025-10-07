import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///./instance/knowledge_base.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-jwt-key'

    # Llama Server URLs
    LLM_URL = os.environ.get('LLM_URL')
    EMBEDDING_URL = os.environ.get('EMBEDDING_URL')
    RERANKING_URL = os.environ.get('RERANKING_URL')

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    # Bing Search API
    BING_SEARCH_URL = os.environ.get('BING_SEARCH_URL')
    BING_API_KEY = os.environ.get('BING_API_KEY')

    # FAISS Index path
    FAISS_INDEX_PATH = "faiss_index"
