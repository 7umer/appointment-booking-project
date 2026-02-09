from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(email="admin@gmail.com").exists():
            User.objects.create_superuser(
                email="admin@gmail.com",
                password="admin123"
            )