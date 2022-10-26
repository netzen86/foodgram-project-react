import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            User.objects.create_superuser(
                username=os.getenv('BE_USERNAME', default='admin'),
                first_name=os.getenv('BE_FNAME', default='Zavulon'),
                last_name=os.getenv('BE_LNAME', default='Ivanovich'),
                is_subscribed=False,
                email=os.getenv('BE_EMAIL', default='admin@yandex.ru'),
                password=os.getenv('BE_PASSWORD', default='p@s$w0rd777')
            )
        else:
            print('Админский акаунт уже создан')
