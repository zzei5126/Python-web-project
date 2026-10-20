from django.apps import AppConfig
from django.core.signals import request_started


class GuestbookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "guestbook"

    def ready(self):
        def initialize_from_json(sender, **kwargs):
            from .services import load_json_into_db
            try:
                load_json_into_db()
            except Exception:
                pass
            request_started.disconnect(initialize_from_json)

        request_started.connect(initialize_from_json)
