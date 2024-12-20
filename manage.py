#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmacia.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    
from django.contrib.auth import get_user_model

User = get_user_model()

# Configura tus datos de superusuario aquí
SUPERUSER_USERNAME = "victor"
SUPERUSER_EMAIL = "va3164070@gmail.com"
SUPERUSER_PASSWORD = "12345"

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(
        username=SUPERUSER_USERNAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD,
    )
    print("Superusuario creado exitosamente.")
else:
    print("El superusuario ya existe.")
