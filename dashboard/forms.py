import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from dashboard.models import VolunteerProfile, OrganisationProfile, OrganisationType, AgeRange, Event


class EditVolunteerProfileForm(forms.ModelForm):
	name = forms.CharField(
		label='Nome completo',
		widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control mb-2'}),
		required=False,
		error_messages={'required': 'Este campo é obrigatório'},
		validators=[RegexValidator('^[a-zA-ZÀ-ÖØ-öø-ÿ]+(([\',. -][a-zA-ZÀ-ÖØ-öø-ÿ ])?[a-zA-ZÀ-ÖØ-öø-ÿ]*)*$',
		                           message='O campo deve apenas conter letras')]
	)

	birth_date = forms.DateField(
		label='Data de nascimento',
		widget=forms.TextInput(attrs={
			'placeholder': 'Data de nascimento',
			'class': 'form-control mb-2',
			'id': 'picker',
		}),
		required=False,
		error_messages={'required': 'Este campo é obrigatório', 'invalid': 'Insira uma data válida'},
	)

	gender = forms.CharField(
		label='Sexo',
		widget=forms.Select(
			choices=[(True, 'Feminino'), (False, 'Masculino')],
		    attrs={'class': 'form-control mb-2', 'placeholder': 'Selecione o seu sexo'}
		),
		error_messages={'required': 'Este campo é obrigatório', 'invalid': 'Selecione uma opção'},
	)

	occupation = forms.CharField(
		label='Ocupação',
		widget=forms.TextInput(attrs={'placeholder': 'Ocupação', 'class': 'form-control mb-2'}),
		required=False,
		error_messages={'invalid': 'Campo inválido'},
		validators=[RegexValidator('[A-Za-zÀ-ÖØ-öø-ÿ]', message='O campo deve apenas conter letras')]
	)

	location = forms.CharField(
		label='Localidade',
		widget=forms.TextInput(attrs={'placeholder': 'Localização', 'class': 'form-control mb-2'}),
		required=False,
		error_messages={'invalid': 'Campo inválido'},
		validators=[RegexValidator('[A-Za-zÀ-ÖØ-öø-ÿ]', message='O campo deve apenas conter letras')]
	)

	phone_number = forms.RegexField(
		regex=r'^\+?1?\d{9,15}$',
	    label='Número de telemóvel',
	    required=False,
	    widget=forms.TextInput(attrs={'placeholder': 'Número de telemóvel', 'class': 'form-control mb-2'}),
		error_messages={'invalid': 'Formato incorreto'})

	image = forms.ImageField(
		label='Foto de perfil',
		required=False,
		widget=forms.FileInput(attrs={'class': 'custom-file-input',	'lang': 'pt', 'id': 'image_input',}),
		error_messages={'invalid': 'A imagem deve ser do tipo jpg/jpeg ou png com tamanho maximo de 4MB'})

	def clean_birth_date(self):
		date = self.cleaned_data['birth_date']
		if date >= datetime.date.today():
			raise ValidationError('Data inválida')
		return date

	def clean_image(self):
		content = self.cleaned_data['image']
		if content:
			if content.size > 4 * 1024 * 1024:
				raise ValidationError('O tamanho da imagem tem de ser inferior a 4MB')
			return content

	class Meta:
		model = VolunteerProfile
		fields = ['name', 'birth_date', 'gender', 'occupation', 'location', 'phone_number', 'image']


class EditOrganisationProfileForm(forms.ModelForm):
	organisation_name = forms.CharField(
		label='Nome da organização',
		widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control mb-2'}),
		error_messages={'required': 'Este campo é obrigatório'},
		validators=[RegexValidator('^[a-zA-ZÀ-ÖØ-öø-ÿ]+(([\',. -][a-zA-ZÀ-ÖØ-öø-ÿ ])?[a-zA-ZÀ-ÖØ-öø-ÿ]*)*$',
		                           message='O campo deve apenas conter letras')]
	)

	representative_name = forms.CharField(
		label='Nome do representante',
		widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control mb-2'}),
		error_messages={'required': 'Este campo é obrigatório'},
		validators=[RegexValidator('^[a-zA-ZÀ-ÖØ-öø-ÿ]+(([\',. -][a-zA-ZÀ-ÖØ-öø-ÿ ])?[a-zA-ZÀ-ÖØ-öø-ÿ]*)*$',
		                           message='O campo deve apenas conter letras')]
	)

	image = forms.ImageField(
		label='Foto da organização',
		required=False,
        widget=forms.FileInput(attrs={'class': 'custom-file-input', 'lang': 'pt', 'id': 'image_input',}),
	    error_messages={'invalid': 'A imagem deve ser do tipo jpg/jpeg ou png com tamanho maximo de 4MB'})

	age_range = forms.ModelMultipleChoiceField(
		label='Alvo(s) da organização',
		queryset=AgeRange.objects.all(),
		widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkboxes'}),
		error_messages={'required': 'Selecione pelo menos uma opção'})

	organisation_type = forms.ModelMultipleChoiceField(
		label='Área(s) de atuação da organização',
		queryset=OrganisationType.objects.all(),
		widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkboxes'}),
		error_messages={'required': 'Selecione pelo menos uma opção'})

	def clean_image(self):
		content = self.cleaned_data['image']
		if content:
			if content.size > 4 * 1024 * 1024:
				raise ValidationError('O tamanho da imagem tem de ser inferior a 4MB')
			return content

	class Meta:
		model = OrganisationProfile
		fields = ['organisation_name', 'representative_name', 'age_range', 'organisation_type', 'image']


class PlanEventForm(forms.ModelForm):
	start = forms.DateTimeField(
		label='Início do evento',
		widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'id': 'pickerStart'}),
		error_messages={'required': 'Por favor dê uma data de início ao evento'},
)

	end = forms.DateTimeField(
		label='Fim do evento',
		widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'id': 'pickerEnd'}),
		error_messages={'required': 'Por favor dê uma data de fim ao evento'},
	)

	title = forms.CharField(
		label='Nome do evento',
		widget=forms.TextInput(attrs={'class': 'form-control mb-2'}),
		error_messages={'required': 'Por favor dê um título ao evento'}
	)

	description = forms.CharField(
		label='Descrição do evento',
		widget=forms.Textarea(attrs={'class': 'form-control mb-2'}),
		error_messages={'required': 'Por favor dê uma descrição ao evento'}
	)

	image = forms.ImageField(label='Foto descritiva do evento',
        required=False,
        widget=forms.FileInput(attrs={'class': 'custom-file-input', 'lang': 'pt', 'id': 'image_input',}),
        error_messages={'invalid': 'A imagem deve ser do tipo jpg/jpeg ou png com tamanho maximo de 4MB'})

	class Meta:
		model = Event
		fields = ['start', 'end', 'title', 'description', 'image']
