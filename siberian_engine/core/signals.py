from django.db.models.signals import post_save
from django.core.cache import cache
from django.dispatch import receiver
from django.conf import settings

from .tasks import order_completed
from .models import Engine, Operation, Order


@receiver(post_save, sender=Engine)
def update_cache_on_engine_save(sender, instance, created, **kwargs):
    if created:
        cache.delete(settings.ENGINE_CACHE_NAME)


@receiver(post_save, sender=Operation)
def clear_cache_on_operation_save(sender, instance, created, **kwargs):
    if created:
        cache.delete(settings.OPERATION_CACHE_NAME)


@receiver(post_save, sender=Order)
def send_email_order_complete(sender, instance, created, **kwargs):
    if instance.status == 'Готов':
        order_completed.delay(instance.id)
