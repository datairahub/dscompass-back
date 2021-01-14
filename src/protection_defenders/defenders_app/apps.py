from django.apps import AppConfig
from django.db.models.signals import post_save


class ProtectionDefendersAppConfig(AppConfig):
    name = 'src.protection_defenders.defenders_app'
    label = 'defenders_app'
    verbose_name = 'Defenders App'

    def ready(self):
        from .models import Question
        from .signals import update_form_length

        post_save.connect(update_form_length, sender=Question)
