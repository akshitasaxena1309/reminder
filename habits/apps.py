import os
from django.apps import AppConfig
from django.conf import settings


class HabitsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "habits"

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true" and getattr(settings, "ENABLE_SCHEDULER", False):
            from habits import scheduler
            scheduler.start()