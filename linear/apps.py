from django.apps import AppConfig


class LinearConfig(AppConfig):
    name = "linear"
    verbose_name = "Linear issues"

    def ready(self) -> None:
        from . import signals  # noqa

        return super().ready()
