import os
from flask import Flask
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

from backend.models import db
from backend.config import Config
# Defer blueprint imports until they are needed
# from backend.auth.routes import auth_bp
# from backend.routes.main import main_bp
# from backend.services.aggregation import run_aggregation_for_all_users

mail = Mail()
cors = CORS()

def create_app(config_class=Config):
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    if app.config.get("TESTING"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        db_path = os.path.join(app.instance_path, 'knowledge_base.db')
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}}) # Example CORS config

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Import and register blueprints
        from backend.auth.routes import auth_bp
        from backend.routes.main import main_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(main_bp, url_prefix='/api')

        # Start the scheduler for background tasks
        from backend.services.aggregation import run_aggregation_for_all_users
        scheduler = BackgroundScheduler(daemon=True)
        # Run job every 6 hours
        scheduler.add_job(run_aggregation_for_all_users, 'interval', hours=6, args=[app])
        scheduler.start()

    return app
