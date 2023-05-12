from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserModel(AbstractUser):
    friends = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Subscribe',
        related_name='you_friends',
    )

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE,
        related_name='you_f',
        verbose_name='Ваш друг'
    )
    author = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE,
        verbose_name='Вы',
    )

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'user'), name='unique_friends'),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Invate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        CustomUserModel,
        related_name='input_invate',
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        CustomUserModel,
        related_name='output_invate',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        constraints = (
            models.UniqueConstraint(
                fields=('sender', 'receiver'), name='unique_invate'),
        )
