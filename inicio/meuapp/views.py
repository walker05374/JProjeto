from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.tokens import default_token_generator
from .forms import ComprovanteForm

from .models import Vacina

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse, JsonResponse
from notifications.signals import notify
import logging

# Import models and forms
from .models import Cliente, CustomUser
from .forms import (
    ClienteForm, 
    ContactMeForm, 
    CustomUser, 
    CustomUserCreationForm, 
    CustomUserChangeForm, 
    CustomUserLoginForm
)
from .utils import google_custom_search
from inicio.meuapp.services import send_mail_to_user

logger = logging.getLogger(__name__)
logger = logging.getLogger('django.request')



# Views
@ratelimit(key='user_or_ip', rate='10/m')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Registra o login tentando
        logger.info(f"Tentativa de login - Usuário: {username}")

        try:
            if '@' in username:
                user = CustomUser.objects.get(email=username)
            else:
                user = CustomUser.objects.get(username=username)
            
            if user.check_password(password):
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                logger.info(f"Login bem-sucedido para o usuário: {username}")  # Log de sucesso
                return redirect('site')  # Redireciona para a página inicial
            else:
                messages.error(request, 'Senha incorreta!')
                logger.warning(f"Falha ao fazer login - Senha incorreta para o usuário: {username}")
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuário não encontrado!')
            logger.warning(f"Falha ao fazer login - Usuário não encontrado: {username}")
    
    return render(request, 'login.html')


@login_required
def site(request):
    # Verifica se o usuário tem clientes cadastrados
    clientes_cadastrados = Cliente.objects.filter(user=request.user).exists()

    # Envia a notificação corretamente
    notify.send(request.user, recipient=request.user, verb=f"Olá {request.user.email}, você está logado")

    # Renderiza a página e passa a variável clientes_cadastrados para o template
    return render(request, 'site.html', {'clientes_cadastrados': clientes_cadastrados})


def registro(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            send_mail_to_user(request=request, user=user)
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')
        else:
            messages.error(request, 'Ocorreu um erro ao cadastrar o usuário. Verifique os campos.')
    
    return render(request, 'register.html', {'form': form})


class MyPasswordReset(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'

    def form_valid(self, form):
        user = form.get_users(form.cleaned_data['email'])[0]
        logger.debug(f"User: {user.username}")
        protocol = 'https' if self.request.is_secure() else 'http'
        domain = self.request.get_host()
        logger.debug(f"Protocol: {protocol}, Domain: {domain}")

        uid = urlsafe_base64_encode(user.pk.encode())
        token = default_token_generator.make_token(user)

        message = render_to_string(self.email_template_name, {
            'user': user,
            'protocol': protocol,
            'domain': domain,
            'uid': uid,
            'token': token,
        })
        send_mail('Redefinição de senha', message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return super().form_valid(form)


class MyPasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class MyPasswordResetConfirm(PasswordResetConfirmView):
    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        return super().form_valid(form)


class MyPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# Contact and feedback views
def contact_me(request):
    if request.method == 'POST':
        form = ContactMeForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('chat')
    else:
        form = ContactMeForm()
    return render(request, 'subChat.html', {'form': form})


def sendmail_contact(data):
    message_body = get_template('send.html').render(data)
    sendmail = EmailMessage(data['subject'], message_body, settings.DEFAULT_FROM_EMAIL, to=['jornadamaternal@gmail.com'])
    sendmail.content_subtype = "html"
    return sendmail.send()


def verify_email(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if not user.email_verified:
        user.email_verified = True
        user.save()
    return redirect('*')


def register(request):
    return render(request, 'registration_form.html')


@login_required
def prenatal(request):
    return render(request, 'abaPreNatal.html')


def mais(request):
    return render(request, 'abaMais.html')


def amamentacao(request):
    return render(request, 'subAmamentacao.html')


def noticias(request):
    return render(request, 'subNoticias.html')


def informacoes(request):
    return render(request, 'adicionarinformacoes.html')


def menu(request):
    return render(request, 'cliente_read.html')


def cep(request):
    return render(request, 'cep.html')


def search_results(request):
    query = request.GET.get('q')
    results = google_custom_search(query) if query else []
    return render(request, 'search_results.html', {'results': results, 'query': query})



def create_cliente(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, request.FILES)
        
        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.user = request.user  # Associar o cliente ao usuário logado
            cliente.save()
            
            # Imprimir a resposta para depuração
            print(f"Cliente criado com sucesso: {cliente}")
            
            # Redireciona para a página de visualizar clientes
            return redirect('read_cliente')
        else:
            # Se o formulário não for válido, mostrar erro
            print("Formulário inválido")
            for field, errors in cliente_form.errors.items():
                print(f"{field}: {errors}")
                
    else:
        cliente_form = ClienteForm()
        
    return render(request, 'cliente_create.html', {'cliente_form': cliente_form})
@login_required
def read_cliente(request):
    clientes = Cliente.objects.filter(user=request.user)  # Filtra pelos clientes do usuário logado
    return render(request, 'cliente_read.html', {'clientes': clientes})

@login_required
def update_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente_form = ClienteForm(request.POST or None, request.FILES or None, instance=cliente)

    if cliente_form.is_valid():
        cliente_form.save()
        return redirect("read_cliente")  # Redireciona para a página de visualizar após atualização

    return render(request, 'cliente_create.html', {'cliente_form': cliente_form})

def delete_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete()

    if not Cliente.objects.exists():
        messages.success(request, "Cadastro da gestante excluído com sucesso. Por favor, atualize suas informações.")
        return redirect("site")  # Se não houver mais clientes cadastrados, redireciona para a página inicial

    messages.success(request, "Cadastro da gestante excluído com sucesso. Por favor, atualize suas informações.")
    return redirect("site")  # Redireciona para a página de visualização de clientes


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
        else:
            messages.error(request, 'Ocorreu um erro ao atualizar o perfil.')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})


@login_required
def excluir_conta(request):
    if request.method == "POST":
        user = request.user
        logout(request)  # Desloga o usuário antes de excluir
        user.delete()  # Exclui o usuário do banco de dados
        return redirect('login')
    return redirect('site')



@login_required
def registrar_vacina(request):
    if request.method == 'POST':
        form = ComprovanteForm(request.POST, request.FILES)
        if form.is_valid():
            vacina = form.save(commit=False)
            vacina.gestante = request.user
            vacina.concluida = True
            vacina.save()
            return redirect('mapa_vacinas')
    else:
        form = ComprovanteForm()

    return render(request, 'registrar_vacina.html', {'form': form})

@login_required
def mapa_vacinas(request):
    vacinas = Vacina.objects.all()
    return render(request, 'mapa_vacinas.html', {'vacinas': vacinas})

def registrar_vacina_nome(request, nome):
    vacina = Vacina.objects.get(nome=nome)
    
    if request.method == 'POST':
        form = ComprovanteForm(request.POST, request.FILES, instance=vacina)
        if form.is_valid():
            vacina.completada = True
            form.save()
            return redirect('mapa_vacinas')
    else:
        form = ComprovanteForm(instance=vacina)

    return render(request, 'registrar_vacina.html', {'form': form, 'vacina': vacina})

@login_required
def enviar_comprovante(request, vacina_id):
    """
    View para anexar o comprovante de vacinação.
    """
    vacina = get_object_or_404(Vacina, id=vacina_id, gestante=request.user)

    if request.method == 'POST':
        if 'comprovante' in request.FILES:
            vacina.comprovante = request.FILES['comprovante']
            vacina.concluida = True
            vacina.save()
            return redirect('mapa_vacinas')
        else:
            return render(request, 'enviar_comprovante.html', {
                'vacina': vacina,
                'error': 'Por favor, selecione uma imagem para o comprovante.'
            })

    return render(request, 'enviar_comprovante.html', {'vacina': vacina})