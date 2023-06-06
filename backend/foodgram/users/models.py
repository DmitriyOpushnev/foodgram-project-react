from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, BooleanField, CharField,
                              CheckConstraint, EmailField, F, ForeignKey,
                              Model, Q, UniqueConstraint)

from api.validators import username_validator, validate_clean_text
from core.limits import Limits
from core.texts import HELP_TEXT_FOR_USER, HELP_TEXT_FOR_USER_EMAIL


class User(AbstractUser):
    """Модель пользователя для приложения Foodgram."""

    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'password',)

    email = EmailField(
        verbose_name='Адрес электронной почты',
        max_length=Limits.USER_MODEL_EMAIL_FIELDS_LENGHT.value,
        unique=True,
        help_text=HELP_TEXT_FOR_USER_EMAIL,
    )

    username = CharField(
        verbose_name='Уникальный юзернейм',
        max_length=Limits.USER_MODEL_OTHER_FIELDS_LENGHT.value,
        unique=True,
        help_text=HELP_TEXT_FOR_USER,
        validators=[username_validator, validate_clean_text],
    )

    first_name = CharField(
        verbose_name='Имя',
        max_length=Limits.USER_MODEL_OTHER_FIELDS_LENGHT.value,
        help_text=HELP_TEXT_FOR_USER,
        validators=[validate_clean_text],
    )

    last_name = CharField(
        verbose_name='Фамилия',
        max_length=Limits.USER_MODEL_OTHER_FIELDS_LENGHT.value,
        help_text=HELP_TEXT_FOR_USER,
        validators=[validate_clean_text],
    )

    password = CharField(
        verbose_name='Пароль',
        max_length=Limits.USER_MODEL_OTHER_FIELDS_LENGHT.value,
        help_text=HELP_TEXT_FOR_USER,
    )

    is_subscribed = BooleanField(
        default=False,
        verbose_name='Активная подписка',
        help_text='Подписаться на пользователя',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscription(Model):
    """Модель подписок на пользователей приложения Foodgram."""

    author = ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='following',
        on_delete=CASCADE,
    )
    user = ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id', )
        constraints = [
            UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscribe'
            ),
            CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_subscribing'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
