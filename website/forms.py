from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Nome de utilizador'),
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Nome de utilizador',
                                      'class': 'form-input-username form-control mb-2'}),
        error_messages={'required': _('Campo obrigatório')},
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Password',
                                          'class': 'form-input-password form-control mb-2'}),
        error_messages={'required': _('Campo obrigatório')},
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Credenciais erradas')
            if not user.check_password(password):
                raise forms.ValidationError('Credenciais erradas')
            if not user.is_active:
                raise forms.ValidationError('Credenciais erradas')
        return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
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

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('As passwords devem ser iguais')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Já existe um utilizador com esse email')

        return super(RegisterForm, self).clean()

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError('Já existe um utilizador com esse nome de utilizador')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError('Já existe um utilizador com esse email')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user
