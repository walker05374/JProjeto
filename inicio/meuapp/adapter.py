from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        # Se a conta já existe (já conectada), deixa o fluxo seguir normal
        if sociallogin.is_existing:
            return
        
        # Se não está conectada, verifica se já temos um usuário com esse email no banco
        user_model = get_user_model()
        email = sociallogin.account.extra_data.get('email')
        
        if email:
            try:
                # Tenta achar o usuário pelo e-mail
                user = user_model.objects.get(email__iexact=email)
                
                # Se achou, conecta a conta do Google a este usuário existente AGORA
                sociallogin.connect(request, user)
                
                # E força o login imediato, pulando qualquer tela de cadastro
                perform_login(request, user, email_verification='none')
                
            except user_model.DoesNotExist:
                # Se o usuário não existe, o allauth vai criá-lo (devido ao AUTO_SIGNUP=True no settings)
                pass