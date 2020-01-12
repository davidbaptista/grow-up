from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = '^[a-zA-Z0-9_]*$'
    message = _('Introduza um nome de utilizador válido. Apenas pode conter letras, números e o caracter \'_\' ')
    flags = 0
