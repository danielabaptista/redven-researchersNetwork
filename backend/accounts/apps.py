from django.apps import AppConfig

class accounts(AppConfig):  
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # change to your app name

    def ready(self):
        import accounts.signals  # 👈 this makes sure signals are loaded
