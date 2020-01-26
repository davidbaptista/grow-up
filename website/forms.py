from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Nome de utilizador',
                                      'class': 'form-input-username form-control mb-2'}),
        error_messages={'required': _('Campo obrigatório')},
    )

    password = forms.CharField(
        label='',
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


class RegisterFormVolunteer(forms.ModelForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de utilizador',
            'class': 'form-control mb-2'
        }),
        error_messages={'required': 'Este campo é obrigatório',
                        'unique': 'Já existe um utilizador com esse nome',
                        'invalid': 'Nome de utilizador inválido: Insira apenas letras e números'},
    )

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control mb-2'
        }),
        error_messages={'required': 'Este campo é obrigatório',
                        'invalid': 'Email inválido',
                        'unique': 'Já existe um utilizador com esse email'},
    )

    error_messages = {
        'password_mismatch': _('As duas palavras passe não são iguais'),
    }

    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control mb-2'
        }),
        help_text=password_validation.password_validators_help_text_html(),
        error_messages={'required': 'Este campo é obrigatório',
                        'password_too_short': 'A password deve ter pelo menos 8 caracteres'},
    )

    password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmação',
            'class': 'form-control mb-2'
        }),
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

        return super(RegisterFormVolunteer, self).clean()

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


class RegisterFormOrganisation(RegisterFormVolunteer):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Email do responsável ou organização',
                                       'class': 'form-control mb-2'}),
        error_messages={'required': 'Este campo é obrigatório',
                        'invalid': 'Email inválido',
                        'unique': 'Já existe um utilizador com esse email'},
    )

class PasswordChangeForm(PasswordChangeForm):
    error_messages = {'password_mismatch': _('As duas passwords não são iguais'),
                      'password_incorrect': _('Password antiga incorreta')}

    old_password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
            'placeholder': 'Password antiga',
            'class': 'form-control mb-2'
        }),
        error_messages={'required': 'Este campo é obrigatório',
                        'password_too_short': 'A password deve ter pelo menos 8 caracteres'},
    )

    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Password nova',
                                          'class': 'form-control mb-2'}),
        error_messages={'required': 'Este campo é obrigatório',
                        'password_too_short': 'A password deve ter pelo menos 8 caracteres'},
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Confirmação da password',
                                          'class': 'form-control mb-2'}),
        error_messages={'required': 'Este campo é obrigatório',
                        'password_too_short': 'A password deve ter pelo menos 8 caracteres'},
    )

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'placeholder': 'Email associado à conta',
                                       'class': 'form-control mb-3'}),
        error_messages={'required': 'Este campo é obrigatório',
                        'invalid': 'Email inválido'}
    )

