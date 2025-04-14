from django.core.management.base import BaseCommand
from inicio.meuapp.models import CustomUser  # Use o CustomUser aqui

class Command(BaseCommand):
    help = 'Cria um superusuário com nome de usuário "1" e senha "1" automaticamente.'

    def handle(self, *args, **kwargs):
        username = '1'
        email = '1@gmail.com'
        password = '1'

        # Verifica se o superusuário já existe
        if not CustomUser.objects.filter(username=username).exists():
            CustomUser.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuário \"{username}\" criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING(f'Superusuário \"{username}\" já existe!'))
