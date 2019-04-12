from django.apps import AppConfig


class MessagingAppConfig(AppConfig):

    name = "enrollment.messaging"
    verbose_name = "Emergency messaging"

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
