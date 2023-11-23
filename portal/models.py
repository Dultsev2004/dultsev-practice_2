from django.db import models
from .validators import FIOValidator, LoginValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    full_name_validator = FIOValidator()
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО',
        validators=[full_name_validator],
        help_text=_('Не больше 255 символов. Только кириллические буквы, дефис и пробелы')
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание категории')

    def __str__(self):
        return self.title


class Application(models.Model):
    date = models.DateTimeField(verbose_name='Временная метка', auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Владелец')
    title = models.CharField(max_length=255, verbose_name='Название звявки')
    description = models.TextField(verbose_name='Описание заявки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='images/', verbose_name='Фото')

    STATE_CHOICES = [
        ('new', 'Новая'),
        ('progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='new', verbose_name='Статус заявки')

    def __str__(self):
        return self.title
