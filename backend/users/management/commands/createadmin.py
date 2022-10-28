import os

from django.core.management.base import BaseCommand
from users.models import CustomUser as User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            print('Создаём админский акаунт')
            User.objects.create_superuser(
                username=os.getenv('BE_USERNAME', default='admin'),
                email=os.getenv('BE_EMAIL', default='admin@yandex.ru'),
                password=os.getenv('BE_PASSWORD', default='p@s$w0rd777'),
            )
        else:
            print('Админский акаунт уже создан')
