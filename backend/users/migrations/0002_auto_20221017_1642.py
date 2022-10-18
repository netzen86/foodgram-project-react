# Generated by Django 2.2.16 on 2022-10-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким username уже существует.'}, help_text=('Обязательное поле. 150 символов или меньше.', 'Буквы, цифры и @/./+/-/_.'), max_length=150, unique=True, verbose_name='Имя пользователя'),
        ),
    ]