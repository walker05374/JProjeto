from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser






class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

class Cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
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

    atualizado_em = models.DateTimeField(auto_now=True)  # Atualiza a cada alteração
    foto = models.ImageField(upload_to='', null=True, blank=True)
    print 




    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"


class ContactMe(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()



class Vacina(models.Model):
    nome = models.CharField(max_length=100, unique=True)  # <- Adiciona o unique=True
    data = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='vacinas/', null=True, blank=True)
    completada = models.BooleanField(default=False)

class Comprovante(models.Model):
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    data_aplicacao = models.DateField()
    imagem = models.ImageField(upload_to='comprovantes/')

    def __str__(self):
        return f"Comprovante de {self.vacina.nome} em {self.data_aplicacao}"