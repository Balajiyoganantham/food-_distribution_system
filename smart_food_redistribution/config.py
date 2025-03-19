import os

class Config:
    """Application Configuration"""

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = r'sqlite:///C:/Users/balaj/db/mydb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # (not used for display here but kept for potential future use)
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "your-google-maps-api-key")

    # Email Configuration (for sending donation confirmation mails)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "NGOFOODREDISTRIBUTION@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "nzym ayax kybn ymal")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "NGOFOODREDISTRIBUTION@gmail.com")

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Debug Mode
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"