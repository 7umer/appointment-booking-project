import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = "admin@gmail.com"
password = "admin123"

user, created = User.objects.get_or_create(email=email)

if created:
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Admin created")
else:
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    print("Admin fixed")
