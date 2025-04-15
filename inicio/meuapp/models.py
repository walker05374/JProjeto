from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import math


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
    NOME_VACINAS = [
        ('BCG', 'BCG'),
        ('Hepatite B', 'Hepatite B'),
        ('DTPa', 'DTPa'),
        ('Influenza', 'Influenza'),
    ]

    nome = models.CharField(max_length=100, choices=NOME_VACINAS)
    data = models.DateField()
    comprovante = models.ImageField(upload_to='comprovantes/')
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class GanhoPeso(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    peso_inicial = models.FloatField()
    peso_atual = models.FloatField()
    altura = models.FloatField()
    semana_gestacional = models.IntegerField()
    imc = models.FloatField()
    classificacao = models.CharField(max_length=20)
    grafico = models.ImageField(upload_to='graficos_gestante/', null=True, blank=True)

    def __str__(self):
        return f"Ganho de Peso - {self.usuario}"
    
from django.db import models

class PostoSaude(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tipo = models.CharField(max_length=100, null=True, blank=True)  # Tipo de serviço (hospital, posto, etc.)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

    def calcular_distancia(self, lat, lng):
        """
        Método para calcular a distância entre o posto de saúde e a localização fornecida (lat, lng)
        Usamos a fórmula de Haversine para calcular a distância em km
        """
        R = 6371  # Raio da Terra em km
        phi1 = math.radians(lat)
        phi2 = math.radians(self.latitude)
        delta_phi = math.radians(self.latitude - lat)
        delta_lambda = math.radians(self.longitude - lng)

        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = R * c
        return distancia        
