from django import forms
from .models import Cliente, ContactMe
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ClienteForm(forms.ModelForm):
    datanascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Cliente
        fields = ['nome', 'datanascimento', 'cpf', 'idadecrianca', 'sus', 'endereco', 'bairro', 'cep', 'cidade', 'uf', 'nomecrianca', 'generocrianca']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'datanascimento': forms.DateInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'idadecrianca': forms.TextInput(attrs={'class': 'form-control'}),
            'sus': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'nomecrianca': forms.TextInput(attrs={'class': 'form-control'}),
            'generocrianca': forms.Select(attrs={'class': 'form-control'}),
        }

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

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
from django import forms
from .models import Cliente, ContactMe
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ClienteForm(forms.ModelForm):
    datanascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Cliente
        fields = ['nome', 'datanascimento', 'cpf', 'idadecrianca', 'sus', 'endereco', 'bairro', 'cep', 'cidade', 'uf', 'nomecrianca', 'generocrianca']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'datanascimento': forms.DateInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'idadecrianca': forms.TextInput(attrs={'class': 'form-control'}),
            'sus': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'nomecrianca': forms.TextInput(attrs={'class': 'form-control'}),
            'generocrianca': forms.Select(attrs={'class': 'form-control'}),
        }

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

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
