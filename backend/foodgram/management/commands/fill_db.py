import csv
import os

from django.conf import settings as set
from django.core.management.base import BaseCommand
from foodgram.models import Ingredients

DATA_DIR = os.path.join(set.BASE_DIR, "data")


class Command(BaseCommand):
    help = 'Заполнение БД'

    def handle(self, *args, **options):
        with open(f'{DATA_DIR}/ingredients.csv', 'r', encoding='utf8') as f:
            dr = csv.reader(f, delimiter=',')
            for row in dr:
                Ingredients.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
            self.stdout.write('Таблица Ingredients заполнена!')
