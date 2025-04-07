from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Cliente, ContactMe,CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import password_validation
from django.forms.widgets import DateInput
from django import forms
from .models import Vacina


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuário',
            'required': 'required',
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha',
            'required': 'required',
        })
    )

    error_messages = {
        'invalid_login': {
            'message': "Usuário e/ou senha inválidos. Por favor, tente novamente.",
        },
        'inactive': {
            'message': "Esta conta está inativa.",
        },
    }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': "O nome de usuário já está em uso. Por favor, escolha outro.",
            },
            'email': {
                'unique': "Este email já está registrado. Por favor, use um email diferente.",
            },
            'password2': {
                'password_mismatch': "As senhas não correspondem. Por favor, verifique novamente.",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "As senhas não correspondem. Por favor, verifique novamente.")

        return cleaned_data




class CustomUserChangeForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'current_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        user = self.instance

        if not user.check_password(current_password):
            raise ValidationError("Senha atual está incorreta.")
        return current_password





class ClienteForm(forms.ModelForm):
    datanascimento = forms.DateField(
        widget=DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
        input_formats=['%Y-%m-%d'],  # ISO format, usado pelo input type="date"
    )

    class Meta:
        model = Cliente
        fields = [
            'nome', 'datanascimento', 'cpf', 'idadecrianca', 'sus',
            'endereco', 'bairro', 'cep', 'cidade', 'uf',
            'nomecrianca', 'generocrianca', 'foto'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'idadecrianca': forms.NumberInput(attrs={'class': 'form-control'}),
            'sus': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'nomecrianca': forms.TextInput(attrs={'class': 'form-control'}),
            'generocrianca': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se for edição e a data estiver definida, formata para o padrão do input
        if self.instance and self.instance.pk and self.instance.datanascimento:
            self.fields['datanascimento'].initial = self.instance.datanascimento.strftime('%Y-%m-%d')

class ContactMeForm(forms.ModelForm):
    class Meta:
        model = ContactMe
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


class VacinaForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = ['nome', 'data', 'comprovante']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nome': forms.Select(attrs={'class': 'form-control'}),
        }