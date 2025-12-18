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
from django.core.paginator import Paginator
from django.db import IntegrityError

import threading
import requests
from urllib.parse import urlencode
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO
import logging

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  

# Django auth
from django.contrib.auth import login, logout, authenticate
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

# Models e Forms
from .models import Cliente, CustomUser, GanhoPeso, Vacina, PostoSaude, Topico, Comentario, Curtida, Relatorio, CalculadoraDPP, Moderador, ContactMe
from .forms import (
    ClienteForm, ContactMeForm, CustomUserCreationForm, CustomUserChangeForm,
    VacinaForm, GanhoPesoForm, CalculadoraDPPForm, TopicoForm, ComentarioForm
)
from .utils import google_custom_search, calcular_distancia
from inicio.meuapp.services import send_mail_to_user

logger = logging.getLogger('django.request')

# --- VIEWS DE AUTENTICAÇÃO ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('site')

    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        
        logger.info(f"Tentativa de login: {username_or_email}")

        try:
            # Verifica se é email ou username
            if '@' in username_or_email:
                user_obj = CustomUser.objects.get(email=username_or_email)
                username_to_auth = user_obj.username
            else:
                user_obj = CustomUser.objects.get(username=username_or_email)
                username_to_auth = user_obj.username
            
            # Autentica
            user = authenticate(request, username=username_to_auth, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('site')
            else:
                messages.error(request, 'Senha incorreta!')
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuário não encontrado!')
    
    return render(request, 'registration/login1.html')


def registro(request):
    if request.user.is_authenticated:
        return redirect('site')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_mail_to_user(request=request, user=user)
            except Exception as e:
                logger.error(f"Erro ao enviar email de boas-vindas: {e}")

            # Loga o usuário automaticamente após o registro
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, 'Usuário criado! Bem-vinda.')
            return redirect('site')
        else:
            messages.error(request, 'Erro no formulário. Verifique os campos.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_cliente(request):
    # Tenta buscar um cliente existente
    try:
        cliente_existente = Cliente.objects.get(user=request.user)
        # Se for GET e já existe, redireciona para leitura
        if request.method == 'GET':
             return redirect('read_cliente')
    except Cliente.DoesNotExist:
        cliente_existente = None

    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, request.FILES, instance=cliente_existente)
        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            messages.success(request, "Cadastro completo com sucesso! Bem-vinda.")
            return redirect('site')
        else:
            messages.error(request, "Erro ao salvar os dados. Verifique o formulário.")
    else:
        cliente_form = ClienteForm()

    return render(request, 'informacaogestante/cliente_create.html', {
        'cliente_form': cliente_form,
        'cliente': cliente_existente
    })


@login_required
def site(request):
    """Página inicial (Dashboard)"""
    cliente = Cliente.objects.filter(user=request.user).first()

    if not cliente:
        messages.info(request, 'Por favor, cadastre suas informações pessoais na aba "Gestante" para acessar o fórum e outras funcionalidades.')
    else:
        if not cliente.aviso_mostrado:
            messages.success(request, 'Olá! Parabéns pelo seu cadastro completo! Aproveite o fórum e as ferramentas.')
            cliente.aviso_mostrado = True
            cliente.save()

    notify.send(request.user, recipient=request.user, verb=f"Olá {request.user.username}, você está logada.")
    return render(request, 'site/site.html', {'clientes_cadastrados': bool(cliente)})

# --- DEMAIS VIEWS ---
@ratelimit(key='user_or_ip', rate='10/m')
def buscar_livros(request):
    livros = []
    query = request.GET.get('query', '').strip()
    
    # --- CONFIGURAÇÃO DO FILTRO DE CONTEXTO ---
    # Aqui definimos as palavras que GARANTEM que o livro é sobre o tema do site.
    # O operador OR diz que o livro deve ter pelo menos um desses termos.
    termos_chave = "gestação OR gravidez OR parto OR puerpério OR amamentação OR recém-nascido OR pré-natal OR cuidados com bebê OR saúde materna"

    # --- CONSTRUÇÃO DA PESQUISA ---
    if query:
        # Se o usuário digitou algo (ex: "alimentação"), a busca será:
        # "alimentação (gestação OR gravidez OR ...)"
        # Isso força o Google a trazer alimentação APENAS dentro desse universo.
        search_expression = f"{query} ({termos_chave})"
    else:
        # Se não digitou nada, traz os destaques gerais do tema
        search_expression = termos_chave

    # Parâmetros para a requisição ao Google Books
    params = {
        'q': search_expression,
        'langRestrict': 'pt',   # Apenas em português
        'printType': 'books',   # Apenas livros
        'maxResults': 40,       # Traz mais resultados para preencher a paginação
        'orderBy': 'relevance'  # Ordenar por relevância
    }

    try:
        # Faz a requisição passando os parâmetros organizados
        google_books_response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
        
        if google_books_response.status_code == 200:
            google_books = google_books_response.json().get('items', [])
            
            for item in google_books:
                info = item.get('volumeInfo', {})
                
                # Tratamento seguro das imagens
                image_links = info.get('imageLinks', {})
                capa = image_links.get('thumbnail') or image_links.get('smallThumbnail') or ''

                # Adiciona à lista apenas se tiver título
                if info.get('title'):
                    livros.append({
                        'title': info.get('title'),
                        'author_name': info.get('authors', ['Autor desconhecido']),
                        'first_publish_year': info.get('publishedDate', 'Data não informada')[:4], # Pega só o ano
                        'url': item.get('id'), # ID para o link do Google Books
                        'cover_i': capa,
                    })
    except Exception as e:
        logger.error(f"Erro ao buscar livros: {e}")

    # Paginação (mantida a lógica de 8 por página)
    paginator = Paginator(livros, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'site/livros_acervo.html', {
        'page_obj': page_obj, 
        'query': query # Retorna a query original para o template (input)
    })

def termos(request):
    return render(request, 'registration/termos2.html')

class MyPasswordReset(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    def form_valid(self, form):
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

@login_required
def contact_me(request):
    if request.method == 'POST':
        form = ContactMeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect('site')
    else:
        form = ContactMeForm()
    return render(request, 'site/subChat.html', {'form': form})

def verify_email(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if not user.email_verified:
        user.email_verified = True
        user.save()
    return redirect('login')

@login_required
def agendamento(request):
    return render(request, 'agendamento/exames.html')

@login_required
def mais(request):
    return render(request, 'site/abaMais.html')

@login_required
def amamentacao(request):
    return render(request, 'site/subAmamentacao.html')

@login_required
def noticias(request):
    return render(request, 'site/subNoticias.html')

@login_required
def informacoes(request):
    return render(request, 'site/adicionarinformacoes.html')

@login_required
def menu(request):
    return render(request, 'informaçãogestante/cliente_read.html')

def cep(request):
    return render(request, 'site/cep.html')

@login_required
def search_results(request):
    query = request.GET.get('q')
    results = google_custom_search(query) if query else []
    return render(request, 'site/search_results.html', {'results': results, 'query': query})

@login_required
def read_cliente(request):
    if not Cliente.objects.filter(user=request.user).exists():
        messages.warning(request, "Você precisa preencher seus dados primeiro.")
        return redirect('create_cliente')
        
    clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'informacaogestante/cliente_read.html', {'clientes': clientes})

@login_required
def update_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id, user=request.user)
    except Cliente.DoesNotExist:
        return redirect('create_cliente')

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
    messages.success(request, "Cadastro excluído com sucesso.")
    return redirect("site")

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
        logout(request)
        user.delete()
        messages.info(request, "Conta excluída permanentemente.")
        return redirect('login')
    return redirect('site')

@login_required
def vacina_create(request):
    form = VacinaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        vacina = form.save(commit=False)
        vacina.usuario = request.user
        vacina.save()
        messages.success(request, "Vacina cadastrada com sucesso!")
        return redirect('vacina_create')

    vacinas = Vacina.objects.filter(usuario=request.user)
    posicoes = [{'top': 15, 'left': 10}, {'top': 25, 'left': 30}, {'top': 40, 'left': 45}, {'top': 55, 'left': 65}]
    circulos = []
    for i in range(len(posicoes)):
        if i < len(vacinas):
            vacina = vacinas[i]
            vacina.top = posicoes[i]['top']
            vacina.left = posicoes[i]['left']
            circulos.append(vacina)
        else:
            circulos.append({'nome': '', 'top': posicoes[i]['top'], 'left': posicoes[i]['left'], 'vazio': True})

    return render(request, 'vacinas/vacina_create1.html', {'form': form, 'vacinas': vacinas, 'circulos': circulos, 'editar': False})

@login_required
def update_vacina(request, id):
    vacina = get_object_or_404(Vacina, pk=id, usuario=request.user)
    form = VacinaForm(request.POST or None, request.FILES or None, instance=vacina)
    if form.is_valid():
        form.save()
        messages.success(request, "Vacina atualizada!")
        return redirect('vacina_create')
    
    vacinas = Vacina.objects.filter(usuario=request.user)
    posicoes = [{'top': 15, 'left': 10}, {'top': 25, 'left': 30}, {'top': 40, 'left': 45}, {'top': 55, 'left': 65}]
    circulos = []
    for i in range(len(posicoes)):
        if i < len(vacinas):
            vacina_item = vacinas[i]
            vacina_item.top = posicoes[i]['top']
            vacina_item.left = posicoes[i]['left']
            circulos.append(vacina_item)
        else:
            circulos.append({'nome': '', 'top': posicoes[i]['top'], 'left': posicoes[i]['left'], 'vazio': True})

    return render(request, 'vacinas/vacina_create1.html', {'form': form, 'vacinas': vacinas, 'circulos': circulos, 'editar': True})

@login_required
def delete_vacina(request, id):
    vacina = get_object_or_404(Vacina, id=id, usuario=request.user)
    vacina.delete()
    messages.success(request, "Vacina excluída!")
    return redirect("vacina_create")

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

            # Gráfico Completo Restaurado
            semanas = [12, 20, 28, 36, 40]
            peso_ganho = ganho.peso_atual - ganho.peso_inicial
            semanas_reais = [12, ganho.semana_gestacional]
            ganho_reais = [0, peso_ganho]

            plt.figure(figsize=(8, 6))
            plt.plot(semanas, curva, label="Faixa Ideal", color="purple", linestyle="--", linewidth=2)
            plt.plot(semanas_reais, ganho_reais, label="Seu ganho", color="green", marker='o', linewidth=2)
            plt.fill_between(semanas, [v - 1.5 for v in curva], [v + 1.5 for v in curva], color='purple', alpha=0.2)
            plt.title("Ganho de Peso Gestacional")
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
            messages.success(request, "Informações salvas!")
            return redirect('ganho_peso')
        else:
            messages.error(request, "Erro no formulário.")
    else:
        form = GanhoPesoForm(instance=ganho)

    return render(request, 'peso/ganho_peso.html', {'form': form, 'ganho': ganho})

@login_required
def excluir_ganho(request, pk):
    ganho = get_object_or_404(GanhoPeso, pk=pk, usuario=request.user)
    ganho.delete()
    messages.success(request, "Registro excluído!")
    return redirect('ganho_peso')

@login_required
def enviar_email_ganho(request, pk):
    if request.method == 'POST':
        ganho = get_object_or_404(GanhoPeso, pk=pk, usuario=request.user)
        email_destino = request.POST.get('email')
        assunto = "Relatório de Ganho de Peso Gestacional"
        corpo = f"Peso inicial: {ganho.peso_inicial} kg\nPeso atual: {ganho.peso_atual} kg\nIMC: {ganho.imc:.2f}\nClassificação: {ganho.classificacao}"
        
        email = EmailMessage(assunto, corpo, settings.EMAIL_HOST_USER, [email_destino])
        if ganho.grafico:
            email.attach_file(ganho.grafico.path)
        
        email_thread = threading.Thread(target=email.send)
        email_thread.start()
        messages.success(request, "E-mail sendo enviado!")
        return redirect('ganho_peso')

@login_required
def mapa_view(request):
    return render(request, 'agendamentos/mapa1.html', {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})

@login_required
def buscar_postos_saude(request):
    try:
        lat = float(request.GET.get("lat"))
        lng = float(request.GET.get("lng"))
        postos = PostoSaude.objects.all()
        postos_com_distancia = []
        for posto in postos:
            distancia = calcular_distancia(lat, lng, posto.latitude, posto.longitude)
            postos_com_distancia.append({'nome': posto.nome, 'endereco': posto.endereco, 'distancia': distancia})
        postos_com_distancia.sort(key=lambda x: x['distancia'])
        return JsonResponse(postos_com_distancia, safe=False)
    except:
        return JsonResponse([], safe=False)

@login_required
def forum(request):
    topicos = Topico.objects.all()
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.usuario = request.user
            topico.save()
            return redirect('forum')
    else:
        form = TopicoForm()
    return render(request, 'forum/forum.html', {'topicos': topicos, 'form': form})

@login_required
def detalhes_topico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    comentarios = topico.comentarios.all()
    curtiu_topico = Curtida.objects.filter(usuario=request.user, topico=topico).exists()
    comentarios_com_curtidas = []
    for comentario in comentarios:
        curtiu = Curtida.objects.filter(usuario=request.user, comentario=comentario).exists()
        comentarios_com_curtidas.append({'comentario': comentario, 'curtiu': curtiu})
    return render(request, 'forum/_detalhes_topico.html', {'topico': topico, 'comentarios': comentarios_com_curtidas, 'curtiu_topico': curtiu_topico})

@login_required
def deletar_topico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    if topico.usuario == request.user or request.user.is_superuser or Moderador.objects.filter(cliente__user=request.user, ativo=True).exists():
        topico.delete()
        return redirect('forum')
    return redirect('detalhes_topico', topico_id=topico.id)

@login_required
def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.cliente.user == request.user or request.user.is_superuser or Moderador.objects.filter(cliente__user=request.user, ativo=True).exists():
        comentario.delete()
    return redirect('detalhes_topico', topico_id=comentario.topico.id)

@login_required
def curtir_conteudo(request, tipo, id_conteudo):
    if tipo == 'topico':
        conteudo = get_object_or_404(Topico, id=id_conteudo)
        existing = Curtida.objects.filter(usuario=request.user, topico=conteudo)
    else:
        conteudo = get_object_or_404(Comentario, id=id_conteudo)
        existing = Curtida.objects.filter(usuario=request.user, comentario=conteudo)
    
    if existing.exists():
        existing.delete()
    else:
        if tipo == 'topico':
            Curtida.objects.create(usuario=request.user, topico=conteudo)
        else:
            Curtida.objects.create(usuario=request.user, comentario=conteudo)
            
    if tipo == 'comentario':
        return redirect('detalhes_topico', topico_id=conteudo.topico.id)
    return redirect('detalhes_topico', topico_id=conteudo.id)

# --- CORREÇÃO DO REPORTAR ---
@login_required
def reportar_conteudo(request, tipo, id_conteudo):
    # Identifica se é Tópico ou Comentário
    if tipo == 'topico':
        conteudo = get_object_or_404(Topico, id=id_conteudo)
    elif tipo == 'comentario':
        conteudo = get_object_or_404(Comentario, id=id_conteudo)
    else:
        return redirect('forum')

    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        if tipo == 'topico':
            Relatorio.objects.create(cliente=request.user, topico=conteudo, motivo=motivo)
            messages.success(request, "Tópico reportado com sucesso.")
            return redirect('detalhes_topico', topico_id=conteudo.id)
        else:
            Relatorio.objects.create(cliente=request.user, comentario=conteudo, motivo=motivo, topico=conteudo.topico)
            messages.success(request, "Comentário reportado com sucesso.")
            return redirect('detalhes_topico', topico_id=conteudo.topico.id)
    
    # IMPORTANTE: Se for GET (clique no botão), mostra a página de confirmação em vez de redirect cego
    return render(request, 'forum/reportar_conteudo.html', {'conteudo': conteudo, 'tipo': tipo})

@login_required
def excluir_relatorio(request, relatorio_id):
    if request.user.is_superuser:
        get_object_or_404(Relatorio, id=relatorio_id).delete()
        messages.success(request, "Relatório excluído.")
    return redirect('ver_relatorios')

@login_required
def comentar_topico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    if request.method == 'POST':
        try:
            cliente = Cliente.objects.get(user=request.user)
        except Cliente.DoesNotExist:
            messages.warning(request, "Para comentar, complete seu cadastro de gestante primeiro.")
            return redirect('create_cliente')

        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.topico = topico
            comentario.cliente = cliente
            comentario.save()
            return redirect('detalhes_topico', topico_id=topico.id)
    return render(request, 'forum/comentar_topico.html', {'form': ComentarioForm(), 'topico': topico})

@login_required
def ver_relatorios(request):
    if not request.user.is_superuser:
        if not Moderador.objects.filter(cliente__user=request.user, ativo=True).exists():
            return redirect('forum')
    relatorios = Relatorio.objects.all().order_by('-data_relatorio')
    return render(request, 'forum/ver_relatorios.html', {'relatorios': relatorios})

@login_required
def formacaobebe(request):
    return render(request, 'formacaobebe/formacaobebe.html')

@login_required
def calcular_dpp(request):
    calculo = None
    cronograma = []

    if request.method == 'POST':
        form = CalculadoraDPPForm(request.POST)
        if form.is_valid():
            calculo = form.save(commit=False)
            calculo.usuario = request.user
            
            calculo.calcular_dpp() 

            if calculo.tipo_calculo == 'DUM':
                data_calculada = calculo.data_input + timedelta(days=7)
                data_calculada = data_calculada + relativedelta(months=9)
                calculo.data_provavel_parto = data_calculada
                calculo.data_concepcao = calculo.data_input + timedelta(days=14)

            elif calculo.tipo_calculo == 'Parto':
                if calculo.data_provavel_parto:
                    calculo.data_input = calculo.data_provavel_parto - relativedelta(months=9)
                    calculo.data_concepcao = calculo.data_provavel_parto - timedelta(days=280)

            hoje = datetime.today().date()
            if calculo.data_input:
                calculo.semanas_gestacao = (hoje - calculo.data_input).days // 7
                calculo.dias_gestacao = (hoje - calculo.data_input).days % 7

                start_date = calculo.data_input
                cronograma = [
                    {'data': start_date, 'idade': '0 semanas', 'evento': 'Data da última menstruação'},
                    {'data': start_date + timedelta(days=14), 'idade': '2 semanas', 'evento': 'Data provável da concepção'},
                    {'data': start_date + timedelta(weeks=5), 'idade': '5 semanas', 'evento': 'O saco gestacional fica visível no ultrassom'},
                    {'data': start_date + timedelta(weeks=7), 'idade': '7 semanas', 'evento': 'Agende sua Ultrassonografia Transvaginal, embrião visível'},
                    {'data': start_date + timedelta(weeks=12), 'idade': '12-13 semanas', 'evento': 'Período ideal para fazer a Ultrassonografia Morfológica de primeiro trimestre'},
                    {'data': start_date + timedelta(weeks=16), 'idade': '16 semanas', 'evento': 'Se não foi possível ver o sexo do bebê com 13 semanas, agora já é bastante seguro'},
                    {'data': start_date + timedelta(weeks=20), 'idade': '20 semanas', 'evento': 'Geralmente nesta fase a mamãe começa a perceber os movimentos do bebê'},
                    {'data': start_date + timedelta(weeks=22), 'idade': '22 semanas', 'evento': 'Agende sua Ultrassonografia Morfológica de segundo trimestre'},
                    {'data': start_date + timedelta(weeks=26), 'idade': '26 semanas', 'evento': 'Período ideal para fazer Ultrassom 3D/4D'},
                    {'data': start_date + timedelta(weeks=28), 'idade': '28 semanas', 'evento': 'Ecocardiografia fetal para avaliar morfologia e função cardíaca'},
                    {'data': start_date + timedelta(weeks=32), 'idade': '32 semanas', 'evento': 'Avaliação da vitalidade fetal e crescimento com Doppler'},
                    {'data': start_date + timedelta(weeks=34), 'idade': '34 semanas', 'evento': 'Caso ocorra um parto prematuro, as chances de sobrevida são boas'},
                    {'data': start_date + timedelta(weeks=37), 'idade': '37 semanas', 'evento': 'Seu bebê já não é mais prematuro, uma ótima notícia caso ele queira nascer'},
                    {'data': start_date + timedelta(weeks=40), 'idade': '40 semanas', 'evento': 'Essa é a data provável do parto'},
                ]

            messages.success(request, "Cálculo realizado com sucesso!")
            return render(request, 'peso/calculadora.html', {'calculo': calculo, 'cronograma': cronograma})

    else:
        form = CalculadoraDPPForm()

    return render(request, 'peso/calculadora.html', {'form': form, 'calculo': calculo})

@login_required
def enviar_email_dpp(request, pk):
    calculo = get_object_or_404(CalculadoraDPP, pk=pk, usuario=request.user)
    if request.method == 'POST':
        email_destino = request.POST.get('email')
        subject = 'Resultado do Cálculo da DPP'
        message = f"Olá!\n\n" \
                  f"Aqui está o seu cálculo da DPP:\n\n" \
                  f"- Data da Última Menstruação: {calculo.data_input}\n" \
                  f"- Tipo de Cálculo: {calculo.tipo_calculo}\n" \
                  f"- Data Provável do Parto: {calculo.data_provavel_parto}\n" \
                  f"- Idade Gestacional: {calculo.semanas_gestacao} semanas e {calculo.dias_gestacao} dias\n\n" \
                  f"Atenciosamente,\n" \
                  f"Equipe Jornada Maternal."
        
        email_thread = threading.Thread(target=send_mail, args=(subject, message, settings.EMAIL_HOST_USER, [email_destino]))
        email_thread.start()
        messages.success(request, "E-mail enviado!")
    return redirect('calculadora_dpp')