# Generated by Django 2.2.16 on 2022-10-29 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0002_auto_20221018_2145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-id',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
    ]
