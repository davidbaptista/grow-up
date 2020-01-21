import re
from difflib import SequenceMatcher

from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, \
    NumericPasswordValidator
from django.core.exceptions import (
    FieldDoesNotExist, ValidationError,
)
from django.utils.translation import gettext as _


class MinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(
                    f"A password é demasiado curta. Deve conter pelo menos {self.min_length} caracteres",

                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            f"A password deve conter pelo menos {self.min_length} caracteres",
        ) % {'min_length': self.min_length}


class UserAttributeSimilarityValidator(UserAttributeSimilarityValidator):

    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("A password é demasiado semelhante a um dos campos"),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _('A password não pode ser semelhante a informação pessoal')


class NumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("A password é unicamente numérica"),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _('A password não pode ser unicamente numérica')
