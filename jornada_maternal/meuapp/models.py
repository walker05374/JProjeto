# meuapp/models.py
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models

class Cliente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    nome = models.CharField(max_length=40, verbose_name='Nome')
    datanascimento = models.DateField(verbose_name='Data de Nascimento')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    idadecrianca = models.IntegerField(verbose_name='Idade da Criança')
    sus = models.CharField(max_length=16, verbose_name='Número SUS')
    endereco = models.CharField(max_length=50, verbose_name='Endereço')
    bairro = models.CharField(max_length=70, verbose_name='Bairro')
    cep = models.CharField(max_length=15, verbose_name='CEP')
    cidade = models.CharField(max_length=30, verbose_name='Cidade')
    uf = models.CharField(max_length=30, verbose_name='UF')
    nomecrianca = models.CharField(max_length=40, verbose_name='Nome da Criança')
    generocrianca = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name='Gênero da Criança')

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"

class ContactMe(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nome')
    email = models.EmailField(max_length=100, verbose_name='Email')
    subject = models.CharField(max_length=100, verbose_name='Assunto')
    message = models.TextField(verbose_name='Mensagem')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  # OTP para verificação
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
