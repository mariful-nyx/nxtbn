from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nxtbn.order'

    def ready(self):
        import nxtbn.order.receivers  # noqa

