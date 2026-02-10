import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email="admin@gmail.com").exists():
    user = User.objects.create_superuser(
        email="admin@gmail.com",
        password="admin123"
    )
    print("Admin created")
else:
    print("Admin already exists")
