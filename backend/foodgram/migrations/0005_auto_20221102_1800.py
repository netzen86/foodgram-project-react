# Generated by Django 2.2.16 on 2022-11-02 18:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0004_auto_20221030_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Так быстро не возможно ничего приготовить!!!')], verbose_name='Время приготовления (в минутах)'),
        ),
    ]
