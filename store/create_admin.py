# store/create_admin.py
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        "admin", "admin@example.com", "Admin1234!"
    )
    print("Admin creado con éxito")
else:
    print("Admin ya existe")
