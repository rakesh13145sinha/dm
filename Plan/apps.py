from django.apps import AppConfig


class PlanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Plan'
    def ready(self):
       import Plan.signals
