from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
import structlog

logger = structlog.getLogger('audit')


@receiver(pre_save)
def audit_log_pre_save(sender, instance, **kwargs):
    logger.info("about to save this instance: %s " % instance)


@receiver(post_save)
def audit_log_post_save(sender, instance, **kwargs):
    logger.info("saved this instance: %s " % instance)


@receiver(pre_delete)
def audit_log_pre_delete(sender, instance, **kwargs):
    logger.info("deleted this instance: %s " % instance)

