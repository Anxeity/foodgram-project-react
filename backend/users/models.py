from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        blank=False,
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        verbose_name='логин',
        max_length=150,
        unique=True,
        help_text='Не более 150 символов.',
    )
    first_name = models.CharField(verbose_name='имя', max_length=150)
    last_name = models.CharField(verbose_name='фамилия', max_length=150)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','password']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        
