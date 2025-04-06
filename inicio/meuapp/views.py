from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.tokens import default_token_generator





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
    CustomUserLoginForm,
    Vacina,
    VacinaForm
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm

@login_required
def create_cliente(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
        return redirect('update_cliente', id=cliente.id)  # Redireciona para edição se já existir
    except Cliente.DoesNotExist:
        cliente = None

    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, request.FILES)
        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            print(f"Cliente criado com sucesso: {cliente}")
            return redirect('read_cliente')
        else:
            print("Formulário inválido")
            for field, errors in cliente_form.errors.items():
                print(f"{field}: {errors}")
    else:
        cliente_form = ClienteForm()

    return render(request, 'cliente_create.html', {
        'cliente_form': cliente_form,
        'cliente': cliente
    })


@login_required
def read_cliente(request):
    clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'cliente_read.html', {
        'clientes': clientes
    })


@login_required
def update_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id, user=request.user)

    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if cliente_form.is_valid():
            cliente_form.save()
            messages.success(request, "Informações atualizadas com sucesso!")
            return redirect("read_cliente")
    else:
        cliente_form = ClienteForm(instance=cliente)

    return render(request, 'cliente_create.html', {
        'cliente_form': cliente_form,
        'cliente': cliente
    })


@login_required
def delete_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id, user=request.user)
    cliente.delete()

    if not Cliente.objects.filter(user=request.user).exists():
        messages.success(request, "Cadastro da gestante excluído com sucesso. Por favor, atualize suas informações.")
        return redirect("site")

    messages.success(request, "Cadastro da gestante excluído com sucesso.")
    return redirect("read_cliente")



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
def vacina_create(request):
    form = VacinaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        vacina = form.save(commit=False)
        vacina.usuario = request.user
        vacina.save()
        return redirect('vacina_create')  # volta para a mesma página com a lista atualizada

    vacinas = Vacina.objects.filter(usuario=request.user)

    posicoes = [
        {'top': 15, 'left': 10},
        {'top': 25, 'left': 30},
        {'top': 40, 'left': 45},
        {'top': 55, 'left': 65},
    ]

    circulos = []
    for i in range(len(posicoes)):
        if i < len(vacinas):
            vacina = vacinas[i]
            vacina.top = posicoes[i]['top']
            vacina.left = posicoes[i]['left']
            circulos.append(vacina)
        else:
            circulos.append({
                'nome': '',
                'top': posicoes[i]['top'],
                'left': posicoes[i]['left'],
                'vazio': True
            })

    return render(request, 'vacina_create.html', {
        'form': form,
        'vacinas': vacinas,
        'circulos': circulos,
        'editar': False
    })

@login_required
def update_vacina(request, id):
    vacina = get_object_or_404(Vacina, pk=id, usuario=request.user)
    form = VacinaForm(request.POST or None, request.FILES or None, instance=vacina)

    if form.is_valid():
        form.save()
        return redirect('vacina_create')

    vacinas = Vacina.objects.filter(usuario=request.user)

    posicoes = [
        {'top': 15, 'left': 10},
        {'top': 25, 'left': 30},
        {'top': 40, 'left': 45},
        {'top': 55, 'left': 65},
    ]

    circulos = []
    for i in range(len(posicoes)):
        if i < len(vacinas):
            vacina = vacinas[i]
            vacina.top = posicoes[i]['top']
            vacina.left = posicoes[i]['left']
            circulos.append(vacina)
        else:
            circulos.append({
                'nome': '',
                'top': posicoes[i]['top'],
                'left': posicoes[i]['left'],
                'vazio': True
            })

    return render(request, 'vacina_create.html', {
        'form': form,
        'vacinas': vacinas,
        'circulos': circulos,
        'editar': True
    })

@login_required
def delete_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id, usuario=request.user)
    vacina.delete()
    return redirect("vacina_create")