from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FIOValidator(validators.RegexValidator):
    regex = r"[а-яёА-ЯЁ\-]+\s+[а-яёА-ЯЁ\-]+(?:\s+[а-яёА-ЯЁ\-]+)?"
    message = _(
        "Введите нормальный ФИО!"
    )

@deconstructible
class LoginValidator(validators.RegexValidator):
    regex = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]?"
    message = _(
        "Введите нормальный логин!"
    )



