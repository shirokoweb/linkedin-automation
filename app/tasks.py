from celery import Celery
from celery.schedules import crontab
import os

celery_app = Celery(
    'linkedin_automation',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
)

celery_app.conf.beat_schedule = {
    'publish-posts': {
        'task': 'app.tasks.publish_scheduled_posts',
        'schedule': crontab(minute='*/15'),
    },
    'collect-analytics': {
        'task': 'app.tasks.collect_analytics',
        'schedule': crontab(hour='*/4'),
    },
}

@celery_app.task(name='app.tasks.publish_scheduled_posts')
def publish_scheduled_posts():
    from app.scheduler import LinkedInScheduler
    scheduler = LinkedInScheduler()
    return scheduler.publish_pending_posts()

@celery_app.task(name='app.tasks.collect_analytics')
def collect_analytics():
    from app.scheduler import LinkedInScheduler
    scheduler = LinkedInScheduler()
    return scheduler.collect_analytics()
