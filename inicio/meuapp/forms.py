from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Cliente, ContactMe,CustomUser,Vacina,GanhoPeso,ExamePosto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import password_validation









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
          label='Data de Nascimento',  # Aqui você define o verbose_name
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d']
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


class GanhoPesoForm(forms.ModelForm):
    class Meta:
        model = GanhoPeso
        fields = ['peso_inicial', 'peso_atual', 'altura', 'semana_gestacional']

EXAMES_CHOICES = [
    ('', 'Selecione o Exame'),
    ('Outro', 'Outro'),  # Opção para o usuário escrever o exame
    ('glicose', 'Exame de Glicose (Curva glicêmica)'),
    ('urina', 'Exame de Urina (Sumário de Urina)'),
    ('ultrassom', 'Ultrassonografia Obstétrica'),
    ('hemograma', 'Exame de Hemograma Completo'),
    ('toxoplasmose', 'Exame de Toxoplasmose'),
    ('rubeola', 'Exame de Rubéola'),
    ('hepatite_b', 'Exame de Hepatite B e C'),
    ('hiv', 'Exame de HIV'),
    ('sifilis', 'Exame de Sífilis'),
    ('papanicolau', 'Exame de Papanicolau'),
    ('fezes', 'Exame de Fezes'),
    ('estriol', 'Exame de Estriol (hormonal)'),
    ('funcao_renal', 'Teste de Função Renal'),
    ('ecg', 'Exame de Eletrocardiograma (ECG)'),
    ('vitaminas', 'Exame de Vitaminas (como a vitamina D)')
]


from django import forms
from .models import ExamePosto, AgendamentoExame

from django import forms

# Lista de exames para gestantes
EXAMES_CHOICES = [
    ('ultrassonografia_obstetrica', 'Ultrassonografia Obstétrica'),
    ('exame_de_sangue', 'Exame de Sangue (Hemograma Completo)'),
    ('teste_de_glicemia', 'Teste de Glicemia'),
    ('exame_de_urina', 'Exame de Urina'),
    ('exame_de_sangue_hiv', 'Exame de Sangue para HIV'),
    ('exame_toxoplasmose', 'Exame de Toxoplasmose'),
    ('exame_hepatite_b', 'Exame de Hepatite B'),
    ('exame_hepatite_c', 'Exame de Hepatite C'),
    ('eletrocardiograma', 'Eletrocardiograma'),
    ('exame_streptococcus', 'Exame de Streptococcus do Grupo B'),
    ('exame_de_vitaminas', 'Exame de Vitaminas e Minerais'),
    ('ecocardiograma_fetal', 'Ecocardiograma Fetal'),
    ('ultra_translucidencia_nucal', 'Ultra-transluminância Nucal (TN)'),
    ('exame_bioquimico', 'Exame de Bioquímica (Função renal e hepática)'),
    ('teste_papanicolau', 'Teste de Papanicolau'),
    ('exame_pressao_arterial', 'Exame de Pressão Arterial'),
    ('monitoramento_cardiaco_fetal', 'Exame de Monitoramento Cardíaco Fetal'),
    ('anticorpos_rubeola', 'Exame de Anticorpos para Rubéola'),
    ('teste_glicose_oral', 'Teste de Glicose Oral'),
    ('testes_geneticos', 'Testes Genéticos e Screening de Anomalias Genéticas'),
    ('exame_dna_fetal', 'Exame de DNA Fetal Não Invasivo'),
]

class SolicitarExameForm(forms.Form):
    exame = forms.ChoiceField(
        choices=EXAMES_CHOICES,  # Lista de exames de gestação
        label="Selecione o Exame"
    )
    posto = forms.ModelChoiceField(
        queryset=ExamePosto.objects.all(),  # Aqui você passa todos os postos armazenados
        label="Selecione o Posto de Saúde"
    )
