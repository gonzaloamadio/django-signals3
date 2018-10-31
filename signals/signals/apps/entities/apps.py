from django.apps import AppConfig


class EntitiesConfig(AppConfig):
    name ='entities'

    def ready(self):
        import entities.signals
