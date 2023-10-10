from django import forms
from .models import Cliente
from .models import ContactMe
from django.contrib.auth.models import AbstractUser
from django.db import models

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'datanascimento', 'cpf', 'idadecrianca',
                  'sus', 'endereco', 'bairro', 'cep', 'cidade', 'uf', 'nomecrianca', 'generocrianca']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Add the otp
    email_verified = models.BooleanField(default=False)
    

    def __str__(self):
        return self.username



