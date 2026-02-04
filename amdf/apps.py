from django.apps import AppConfig


class AmdfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'amdf'

    def ready(self):
        import amdf.signals  # importa os sinais(signals) ao iniciar o projeto
