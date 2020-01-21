from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label=_('Nome de utilizador'),
        error_messages={'required': 'Este campo é obrigatório',
                        'unique': 'Já existe um utilizador com esse nome',
                        'invalid': 'Nome de utilizador inválido: Insira apenas letras e números'},
    )

    email = forms.EmailField(
        label=_('Email'),

        error_messages={'required': 'Este campo é obrigatório',
                        'invalid': 'Email inválido',
                        'unique': 'Já existe um utilizador com esse email'},
    )

    error_messages = {
        'password_mismatch': _('As duas palavras passe não são iguais'),
    }

    password1 = forms.CharField(
        label=_('Palavra passe'),
        strip=False,
        widget=forms.PasswordInput(),
        help_text=password_validation.password_validators_help_text_html(),
        error_messages={'required': 'Este campo é obrigatório',
                        'password_too_short': 'A password deve ter pelo menos 8 caracteres'},
    )

    password2 = forms.CharField(
        label=_('Confirmação da palavra passe'),
        strip=False,
        widget=forms.PasswordInput(),
        error_messages={'required': 'Este campo é obrigatório',
                        'password_too_short': 'A password deve ter pelo menos 8 caracteres'},
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError('Já existe um utilizador com esse email')

        return email
