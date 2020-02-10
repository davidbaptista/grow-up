from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from dashboard.models import VolunteerProfile
from grow_up import settings


class EditVolunteerProfileForm(forms.ModelForm):
	first_name = forms.CharField(
		label='Primeiro nome',
		widget=forms.TextInput(attrs={
			'placeholder': 'Nome',
			'class': 'form-control mb-2'
		}),
		error_messages={'required': 'Este campo é obrigatório'},
		validators=[RegexValidator('[A-Za-zÀ-ÖØ-öø-ÿ]', message='O campo deve apenas conter letras')]
	)

	last_name = forms.CharField(
		label='Último nome',
		widget=forms.TextInput(attrs={
			'placeholder': 'Apelido',
			'class': 'form-control mb-2'
		}),
		error_messages={'required': 'Este campo é obrigatório'},
		validators=[RegexValidator('[A-Za-zÀ-ÖØ-öø-ÿ]', message='O campo deve apenas conter letras')]
	)

	birth_date = forms.DateField(
		label='Data de nascimento (Dia/Mês/Ano)',
		widget=forms.DateInput(format='%d/%m/%Y', attrs={
			'placeholder': 'Data de nascimento (dia/mês/ano)',
			'class': 'form-control mb-2'
		}),
		required=False,
		input_formats=settings.DATE_INPUT_FORMATS,
		error_messages={'required': 'Este campo é obrigatório', 'invalid': 'Insira uma data válida'},
	)

	gender = forms.CharField(
		label='Sexo',
		widget=forms.Select(choices=[('', 'Selecione o sexo'), (True, 'Feminino'), (False, 'Masculino')],
		                    attrs={'class': 'form-control mb-2', 'placeholder': 'Selecione o seu sexo'}),
		error_messages={'required': 'Este campo é obrigatório', 'invalid': 'Selecione uma opção'},
	)

	occupation = forms.CharField(
		label='Ocupação',
		widget=forms.TextInput(attrs={
			'placeholder': 'Ocupação',
			'class': 'form-control mb-2'
		}),
		required=False,
		error_messages={'invalid': 'Campo inválido'},
		validators=[RegexValidator('[A-Za-zÀ-ÖØ-öø-ÿ]', message='O campo deve apenas conter letras')]
	)

	location = forms.CharField(
		label='Localidade',
		widget=forms.TextInput(attrs={
			'placeholder': 'Localização',
			'class': 'form-control mb-2'
		}),
		required=False,
		error_messages={'invalid': 'Campo inválido'},
		validators=[RegexValidator('[A-Za-zÀ-ÖØ-öø-ÿ]', message='O campo deve apenas conter letras')]
	)

	phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
	                                label='Número de telemóvel',
	                                required=False,
	                                widget=forms.TextInput(attrs={
		                                'class': 'form-control mb-2',
	                                }),
	                                error_messages={'invalid': 'Formato incorreto'})

	image = forms.ImageField(label='Selecionar foto de perfil',
	                        required=False,
	                        widget=forms.FileInput(attrs={
		                        'id': 'image',
		                        'class': 'hidden'
	                        }),
	                        error_messages={'invalid': 'A imagem deve ser do tipo jpg/jpeg ou png com tamanho maximo '
	                                                   'de 4MB'})

	def clean_image(self):
		content = self.cleaned_data['image']
		if content:
			if content.size > 4 * 1024 * 1024:
				raise ValidationError('O tamanho da imagem tem de ser inferior a 4MB')
			return content
		else:
			raise ValidationError('Erro a ler a imagem')

	class Meta:
		model = VolunteerProfile
		fields = ['first_name', 'last_name', 'birth_date', 'gender', 'occupation', 'location', 'phone_number', 'image']


class EditOrganisationProfileForm:
	pass
