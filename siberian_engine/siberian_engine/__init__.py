from .celery import app as celery_app


__all__ = ['celery_app']
celery_app.conf.broker_connection_retry_on_startup = True
