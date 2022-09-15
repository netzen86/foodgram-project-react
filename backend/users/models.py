from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES_ROLE = (
    ("user", "user"),
    ("admin", "admin"),
)


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Обязательное поле. 150 символов или меньше.',
                   'Буквы, цифры и @/./+/-/_.'),
        error_messages={
            'unique': "Пользователь с таким username уже существует.",
        },
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "Пользователь с таким email уже существует.",
        },
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    is_subscribed = models.BooleanField(
        verbose_name='Подписан ли текущий пользователь на этого'
    )
    role = models.CharField(
        max_length=10,
        default="user",
        choices=CHOICES_ROLE,
    )

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
