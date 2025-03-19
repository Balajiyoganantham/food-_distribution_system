from celery import Celery
from config import Config
from app import create_app, db
from app.models import Donation
from datetime import datetime

def make_celery(app):
    celery = Celery(app.import_name, broker=Config.CELERY_BROKER_URL)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

flask_app = create_app()
celery = make_celery(flask_app)

@celery.task
def update_donations_status():
    """
    Background task to update donation statuses.
    For example, you might mark donations as expired if they're older than a certain period.
    """
    now = datetime.utcnow()
    donations = Donation.query.all()
    for donation in donations:
        # Add custom logic to update status if needed, e.g.:
        # if (now - donation.created_at).days > 7:
        #     donation.status = "Expired"
        pass
    db.session.commit()
