from django.apps import AppConfig
from django.db.models import signals


class HotplaceConfig(AppConfig):
    name = 'hotplace'

    def ready(self):
        from hotplace.models import (
            Review,
        )
        from hotplace.signals import renewal_rage_avg_when_post_new_review
        signals.post_save.connect(renewal_rage_avg_when_post_new_review, sender=Review)
