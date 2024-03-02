from django.db.models.signals import post_save
from django.core.cache import cache
from django.dispatch import receiver
from django.conf import settings

from .models import Engine, Operation


@receiver(post_save, sender=Engine)
def update_cache_on_engine_save(sender, instance, created, **kwargs):
    if created:
        cache.delete(settings.ENGINE_CACHE_NAME)


@receiver(post_save, sender=Operation)
def clear_cache_on_operation_save(sender, instance, created, **kwargs):
    if created:
        cache.delete(settings.OPERATION_CACHE_NAME)
