from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from .utils import google_custom_search
from .models import Cliente,CustomUser
from django.shortcuts import redirect, render
from django.db.models.signals import post_save
from django.core.mail import send_mail  
from inicio.meuapp.services import send_mail_to_user
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserLoginForm
from django.http import HttpResponse
from notifications.signals import notify





from .forms import (
 
    ClienteForm,
    ContactMeForm,
    CustomUser,
    CustomUserCreationForm,
    CustomUserChangeForm,

        #GestanteForm,
        CustomUserLoginForm,


 
     
)
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
    PasswordResetDoneView,

)




@ratelimit(key='user_or_ip', rate='10/m')





def login_view(request):
    form = CustomUserLoginForm(request, data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('site')  # Redirecione para a página inicial ou outra página
        messages.success(request, 'Login realizado com sucesso!')
    return render(request, 'login.html', {'form': form})



def registro(request):

    template_name = 'register.html'
    form = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            send_mail_to_user(request=request, user=user)
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')  # Redireciona após a mensagem ser adicionada
        else:
            messages.error(request, 'Ocorreu um erro ao cadastrar o usuário. Verifique os campos.')

    return render(request, template_name, {'form': form})



class MyPasswordReset(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
class MyPasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
class MyPasswordResetConfirm(PasswordResetConfirmView):
    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        return super().form_valid(form)
class MyPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

def contact_me(request):
    return render(request, 'subChat.html')

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

def contact_me(request):
    if request.method == 'POST':
        form = ContactMeForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'subject': request.POST.get('subject'),
                'message': request.POST.get('message'),
            }

            sendmail_contact(data) 
            return redirect('contact')
    else:
        form = ContactMeForm()
    return render(request, 'subChat.html', {'form': form})

def sendmail_contact(data):
    message_body = get_template('send.html').render(data)
    sendmail = EmailMessage(data['subject'],
                            message_body, settings.DEFAULT_FROM_EMAIL,
                            to=['jornadamaternal@gmail.com'])
    sendmail.content_subtype = "html"
    return sendmail.send()

def verify_email(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if not user.email_verified:
     #   user.email_verified = True
        user.save()
    return redirect('*') 

def register(request):
    return render(request, 'registration_form.html')
def site(request):
    clientes_cadastrados = Cliente.objects.exists() 
    return render(request, 'site.html', {'clientes_cadastrados': clientes_cadastrados})
def vacina(request):
    return render(request, 'abaVacina.html')
@login_required
def historico_vacina(request):
    return render(request, 'historico_vacina.html')
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
    context = {'results': results, 'query': query}
    return render(request, 'search_results.html', context)

@login_required
def create_cliente(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, request.FILES)
        if cliente_form.is_valid():
            cliente_form.save()
            return redirect("read_cliente")
    else:
        cliente_form = ClienteForm()
    return render(request, 'cliente_create.html', {'cliente_form': cliente_form})

@login_required
def read_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente_read.html', {'clientes': clientes})


@login_required
def update_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente_form = ClienteForm(request.POST or None, request.FILES or None, instance=cliente)
    
    if cliente_form.is_valid():
        cliente_form.save()
        return redirect("read_cliente")  # Certifique-se de que esse nome corresponde ao seu urls.py

    return render(request, 'cliente_create.html', {'cliente_form': cliente_form})

@login_required
def delete_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete()

    # Se não houver mais clientes cadastrados, redireciona para 'site'
    if not Cliente.objects.exists():
        return redirect("site")  # Certifique-se de que existe essa rota no seu urls.py

    return redirect("read_cliente")  # Se ainda houver clientes, volta para a listagem

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
def Gestante(request):
    if request.method == 'POST':
        form = GestanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('historico_vacina')
    else:
        form = GestanteForm()
    return render(request, 'historico_vacina.html', {'form': form})

@login_required
def gestantes_view(request):
    gestantes = Gestante.objects.all()  
    return render(request, 'historico_vacina.html', {'Gestantes': gestantes})
    print(gestantes)  


@login_required
def historico_vacina_ler(request):
    Gestante = Gestante.objects.all()
    return render(request, 'historico_vacina_ler.html', {'Gestante': Gestante})


def account_activation_email(request):
    return render(request, 'account_activation_email.html')