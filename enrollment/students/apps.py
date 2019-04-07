from django.apps import AppConfig


class StudentsAppConfig(AppConfig):

    name = "enrollment.students"
    verbose_name = "Students"

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
