from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""

    CHOICES_ROLE = (
        ('user', 'пользователь'),
        ('admin', 'администратор'),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Обязательное поле. 150 символов или меньше.',
                   'Буквы, цифры и @/./+/-/_.'),
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
        },
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.',
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
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Подписан ли текущий пользователь на этого'
    )
    role = models.CharField(
        choices=CHOICES_ROLE,
        default='user',
        max_length=25,
        verbose_name='Роль пользователя',
    )
    follower = models.ManyToManyField(
        'self',
        blank=True,
        related_name='following',
        symmetrical=False,
        verbose_name='Подписчик',
    )
    favorite = models.ManyToManyField(
        'foodgram.Recipe',
        blank=True,
        related_name='users_favorited',
        verbose_name='Находится ли в избранном',
    )
    cart = models.ManyToManyField(
        'foodgram.Recipe',
        blank=True,
        related_name='users_added_to_cart',
        verbose_name='Находится ли в корзине',
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_subscribed', 'email']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
