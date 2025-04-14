# Django core
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.utils.http import urlsafe_base64_encode
from django.core.serializers.json import DjangoJSONEncoder
import json
from inicio.meuapp.choices import NOME_EXAMES
import math
import requests
from urllib.parse import urlencode




# Django auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

# Terceiros
from django_ratelimit.decorators import ratelimit
from notifications.signals import notify

# Bibliotecas padrão / externas
import os
import logging
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Solução para evitar erros com Tkinter em servidores

# Models
from .models import Cliente, CustomUser, GanhoPeso, Vacina

# Forms
from .forms import (
    ClienteForm,
    ContactMeForm,
    CustomUser,
    CustomUserCreationForm,
    CustomUserChangeForm,
    VacinaForm,
    GanhoPesoForm
    
)

# Utilitários internos
from .utils import google_custom_search
from inicio.meuapp.services import send_mail_to_user

# Logger
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
    
    return render(request, 'registration/login.html')


@login_required
def site(request):
    # Verifica se o usuário tem clientes cadastrados
    clientes_cadastrados = Cliente.objects.filter(user=request.user).exists()

    # Envia a notificação corretamente
    notify.send(request.user, recipient=request.user, verb=f"Olá {request.user.email}, você está logado")

    # Renderiza a página e passa a variável clientes_cadastrados para o template
    return render(request, 'site/site.html', {'clientes_cadastrados': clientes_cadastrados})


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
    
    return render(request, 'registration/register.html', {'form': form})


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
    return render(request, 'site/subChat.html', {'form': form})


def sendmail_contact(data):
    message_body = get_template('site/send.html').render(data)
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
    return render(request, 'registration/registration_form.html')


@login_required
def agendamento(request):
    return render(request, 'agendamento/exames.html')


def mais(request):
    return render(request, 'site/abaMais.html')


def amamentacao(request):
    return render(request, 'site/subAmamentacao.html')


def noticias(request):
    return render(request, 'site/subNoticias.html')


def informacoes(request):
    return render(request, 'site/adicionarinformacoes.html')


def menu(request):
    return render(request, 'informaçãogestante/cliente_read.html')


def cep(request):
    return render(request, 'site/cep.html')


def search_results(request):
    query = request.GET.get('q')
    results = google_custom_search(query) if query else []
    return render(request, 'site/search_results.html', {'results': results, 'query': query})




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

    return render(request, 'informacaogestante/cliente_create.html', {
        'cliente_form': cliente_form,
        'cliente': cliente
    })


def read_cliente(request):
    clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'informacaogestante/cliente_read.html', {'clientes': clientes})


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

    return render(request, 'informacaogestante/cliente_create.html', {
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

    return render(request, 'registration/update_profile.html', {'form': form})


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

    return render(request, 'vacinas/vacina_create.html', {
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

    return render(request, 'vacinas/vacina_create.html', {
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



def calcular_imc(peso, altura=1.60):  # altura padrão, ou pode puxar do perfil do usuário
    return round(peso / (altura ** 2), 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Baixo peso (Você começou a gestação com peso abaixo do ideal. O ganho de peso deve ser mais acompanhado para garantir o bom desenvolvimento do bebê.)"
    elif 18.5 <= imc < 25:
        return "Eutrofia (Você iniciou a gestação com peso considerado adequado. Mantenha uma alimentação equilibrada e continue acompanhando seu ganho de peso.)"
    elif 25 <= imc < 30:
        return "Sobrepeso (Você começou a gestação acima do peso ideal. É importante monitorar o ganho de peso para evitar complicações.)"
    else:
        return "Obesidade (Você iniciou a gestação com obesidade. Acompanhar o ganho de peso é essencial para sua saúde e a do bebê.)"



@login_required
def ganho_peso_view(request):
    try:
        ganho = GanhoPeso.objects.get(usuario=request.user)
    except GanhoPeso.DoesNotExist:
        ganho = None

    if request.method == 'POST':
        form = GanhoPesoForm(request.POST, request.FILES, instance=ganho)
        if form.is_valid():
            ganho = form.save(commit=False)
            ganho.usuario = request.user
            ganho.imc = ganho.peso_inicial / (ganho.altura ** 2)

            # Classificação IMC
            if ganho.imc < 18.5:
                ganho.classificacao = "Baixo peso"
                curva = [0.0, 4.5, 9.0, 11.5, 12.5]
            elif 18.5 <= ganho.imc < 25:
                ganho.classificacao = "Eutrofia"
                curva = [0.0, 4.0, 8.0, 11.0, 12.0]
            elif 25 <= ganho.imc < 30:
                ganho.classificacao = "Sobrepeso"
                curva = [0.0, 3.0, 6.0, 8.0, 9.0]
            else:
                ganho.classificacao = "Obesidade"
                curva = [0.0, 2.0, 4.0, 5.5, 6.0]

            # Gráfico
            semanas = [12, 20, 28, 36, 40]
            peso_ganho = ganho.peso_atual - ganho.peso_inicial
            semanas_reais = [12, ganho.semana_gestacional]
            ganho_reais = [0, peso_ganho]

            plt.figure(figsize=(8, 6))
            plt.plot(semanas, curva, label="Faixa Ideal", color="purple", linestyle="--", linewidth=2)
            plt.plot(semanas_reais, ganho_reais, label="Seu ganho", color="green", marker='o', linewidth=2)
            plt.fill_between(semanas, [v - 1.5 for v in curva], [v + 1.5 for v in curva], color='purple', alpha=0.2)
            plt.title("Ganho de Peso Gestacional (Comparativo com faixa ideal)")
            plt.xlabel("Semanas de Gestação")
            plt.ylabel("Ganho de Peso (kg)")
            plt.grid(True)
            plt.legend()

            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            file_name = f"grafico_{request.user.id}.png"
            ganho.grafico.save(file_name, ContentFile(buffer.read()), save=False)
            buffer.close()
            plt.close()

            ganho.save()
            messages.success(request, "Informações salvas com sucesso!")
            return redirect('ganho_peso')
        else:
            messages.error(request, "Erro ao enviar os dados. Verifique o formulário.")
    else:
        form = GanhoPesoForm(instance=ganho)

    return render(request, 'peso/ganho_peso.html', {
        'form': form,
        'ganho': ganho
    })


@login_required
def excluir_ganho(request, pk):
    ganho = get_object_or_404(GanhoPeso, pk=pk, usuario=request.user)
    ganho.delete()
    messages.success(request, "Registro de ganho de peso excluído com sucesso!")
    return redirect('ganho_peso')


@login_required
def enviar_email_ganho(request, pk):
    if request.method == 'POST':
        ganho = get_object_or_404(GanhoPeso, pk=pk, usuario=request.user)
        email_destino = request.POST.get('email')

        assunto = "Relatório de Ganho de Peso Gestacional"
        corpo = f"""
Olá!

Aqui estão os dados do seu acompanhamento de ganho de peso gestacional:

- Peso inicial: {ganho.peso_inicial} kg
- Peso atual: {ganho.peso_atual} kg
- IMC: {ganho.imc:.2f}
- Classificação: {ganho.classificacao}

Em anexo está o gráfico comparativo com a faixa ideal de ganho de peso.

Atenciosamente,
Equipe de acompanhamento gestacional.
        """

        email = EmailMessage(assunto, corpo, settings.EMAIL_HOST_USER, [email_destino])
        if ganho.grafico:
            email.attach_file(ganho.grafico.path)

        try:
            email.send()
            messages.success(request, "E-mail enviado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao enviar o e-mail: {e}")

        return redirect('ganho_peso')
    

def mapa_view(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'agendamentos/mapa.html', context)


def buscar_postos_saude(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    key = settings.GOOGLE_MAPS_API_KEY

    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query=posto+de+saúde+hospital+SUS+SESMA+AME+exames+posto+de+saúde+público"
        f"&location={lat},{lng}&radius=140000&key={key}"
    )

    response = requests.get(url)
    return JsonResponse(response.json().get("results", []), safe=False)


def gerar_pontos_radiais(lat, lng, raio_km=140, passo_km=50):
    pontos = []
    R = 6371  # Raio da Terra em km

    # Gera uma grade simples em torno do ponto central
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            offset_lat = (passo_km * dy) / R * (180 / math.pi)
            offset_lng = (passo_km * dx) / (R * math.cos(math.radians(lat))) * (180 / math.pi)
            nova_lat = lat + offset_lat
            nova_lng = lng + offset_lng
            pontos.append((nova_lat, nova_lng))

    return pontos
def busca_ampla_postos(lat, lng):
    key = settings.GOOGLE_MAPS_API_KEY
    termos_busca = [
        "posto de saúde",
        "hospital",
        "SUS",
        "SESMA",
        "AME",
        "exames",
        "posto de saúde público"
    ]
    query = "+OR+".join([t.replace(" ", "+") for t in termos_busca])

    pontos = gerar_pontos_radiais(lat, lng)
    resultados_unicos = {}

    for ponto_lat, ponto_lng in pontos:
        url = (
            f"https://maps.googleapis.com/maps/api/place/textsearch/json"
            f"?query={query}&location={ponto_lat},{ponto_lng}&radius=50000&key={key}"
        )

        response = requests.get(url)
        data = response.json()

        for result in data.get("results", []):
            place_id = result.get("place_id")
            if place_id and place_id not in resultados_unicos:
                resultados_unicos[place_id] = result

    return list(resultados_unicos.values())
def proxy_google_amplo(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    key = settings.GOOGLE_MAPS_API_KEY

    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query=posto+de+saúde+OR+ame+sus+OR+sesma+OR+hospital+OR+exames+OR+posto+de+saude+publico"
        f"&location={lat},{lng}&radius=140000&key={key}"
    )

    response = requests.get(url)
    return JsonResponse(response.json())
