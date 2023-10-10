# Imports organizados e remoção de imports duplicados
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import google_custom_search
from .forms import ClienteForm, ContactMeForm , CustomUser 
from .models import Cliente
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from .admin import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.shortcuts import redirect



def site(request):
    return render(request, 'site.html')
    
@login_required
def vacina(request):
    return render(request, 'abaVacina.html')

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
    if query:
        results = google_custom_search(query)
    else:
        results = []
    context = {'results': results, 'query': query}
    return render(request, 'search_results.html', context)



@login_required
def create_cliente(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, request.FILES)
        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.save()
            return redirect("read_cliente")
    else:
        cliente_form = ClienteForm()

    return render(request, 'cliente_create.html', {'cliente_form': cliente_form})


@login_required
def read_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente_read.html', {'clientes':clientes})

@login_required
def update_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente_form = ClienteForm(request.POST or None,
                               request.FILES or None,
                               instance=cliente)
    if(cliente_form.is_valid()):
        cliente = cliente_form.save(commit=False)
        cliente.save()
        return redirect("read_cliente")
    return render(request, 'cliente_create.html', {'cliente_form':cliente_form})
@login_required
def delete_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete()
    return redirect("read_cliente")





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

            # data, puxo as informações dos campos name, email, subject.
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'subject': request.POST.get('subject'),
                'message': request.POST.get('message'),
            }

            sendmail_contact(data)  # Aqui vou criar uma função para envio
            # chamei de sendmail_contact

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



# accounts/views.py
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView
)
from django.shortcuts import redirect, render

from jornada_maternal.app.services import send_mail_to_user

from .forms import CustomUserForm


def signup(request):
    '''
    Cadastra Usuário.
    '''
    template_name = 'registration/registration_form.html'
    form = CustomUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            send_mail_to_user(request=request, user=user)
            return redirect('login')

    return render(request, template_name)


class MyPasswordResetConfirm(PasswordResetConfirmView):
    '''
    Requer password_reset_confirm.html
    '''

    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        return super(MyPasswordResetConfirm, self).form_valid(form)


class MyPasswordResetComplete(PasswordResetCompleteView):
    '''
    Requer password_reset_complete.html
    '''
    ...
