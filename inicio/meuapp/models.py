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


    aviso_mostrado = models.BooleanField(default=False, verbose_name="Aviso mostrado ao usuário")



    atualizado_em = models.DateTimeField(auto_now=True)  # Atualiza a cada alteração
    foto = models.ImageField(upload_to='', null=True, blank=True)


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
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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


##################
#forum
class Moderador(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.cliente.username} (Moderador)'


class Topico(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relacionando ao CustomUser
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)  # Para ativar/desativar tópicos

    def __str__(self):
        return self.titulo
    

# models.py
class Comentario(models.Model):
    texto = models.TextField()
    cliente = models.ForeignKey('Cliente', related_name='comentarios', on_delete=models.CASCADE)
    topico = models.ForeignKey(Topico, related_name='comentarios', on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    resposta = models.ForeignKey('self', null=True, blank=True, related_name='respostas', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comentário de {self.cliente.nome}'


class Curtida(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='curtidas', on_delete=models.CASCADE)
    topico = models.ForeignKey(Topico, related_name='curtidas', null=True, blank=True, on_delete=models.CASCADE)
    comentario = models.ForeignKey(Comentario, related_name='curtidas', null=True, blank=True, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que o usuário só possa curtir o mesmo tópico ou comentário uma vez
        unique_together = ('usuario', 'topico', 'comentario')

    def __str__(self):
        return f'{self.usuario.username} curtiu'



class Relatorio(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    motivo = models.TextField()
    topico = models.ForeignKey(Topico, null=True, blank=True, on_delete=models.CASCADE)
    comentario = models.ForeignKey(Comentario, null=True, blank=True, on_delete=models.CASCADE)
    data_relatorio = models.DateTimeField(auto_now_add=True)
