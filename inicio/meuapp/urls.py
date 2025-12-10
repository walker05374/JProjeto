from django.urls import path, include
from rest_framework import routers
from .viewsets import ClienteViewSet
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from . import views 

router = routers.DefaultRouter()
router.register(r'cliente', ClienteViewSet, basename="Cliente")

urlpatterns = [
    # Autenticação
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'), # Usando sua view personalizada
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')), # URLs do Allauth (social)

    # Site Principal
    path('', views.site, name='site'),
    
    # Cliente / Gestante (Dados adicionais)
    path('create_cliente/', views.create_cliente, name='create_cliente'),
    path('read_cliente/', views.read_cliente, name='read_cliente'),
    path("update_cliente/<int:id>/", views.update_cliente, name='update_cliente'),
    path("delete_cliente/<int:id>", views.delete_cliente, name='delete_cliente'),

    # Funcionalidades
    path('informacoes/', views.informacoes, name='informacoes'),
    path('mais/', views.mais, name='mais'),
    path('amamentacao/', views.amamentacao, name='amamentacao'),
    path('noticias/', views.noticias, name='noticias'),
    path('search/', views.search_results, name='search_results'),
    path('menu/', views.menu, name='menu'),
    path('cep/', views.cep, name='cep'),
    path('contact/', views.contact_me, name='contact'),
    path('termos/', views.termos, name='termos'),

    # Perfil e Senha
    path('update_profile/', views.update_profile, name='update_profile'),
    path('excluir-conta/', views.excluir_conta, name='excluir-conta'),
    path('verify_email/<int:pk>/', views.verify_email, name='verify_email'),
    
    path('reset-password/', views.MyPasswordReset.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetComplete.as_view(), name='password_reset_complete'),

    # Vacinas
    path("create_vacina/", views.vacina_create, name="vacina_create"),
    path("update_vacina/<int:id>/", views.update_vacina, name="update_vacina"),
    path("delete_vacina/<int:id>/", views.delete_vacina, name="delete_vacina"),

    # Peso e Saúde
    path('ganho_peso/', views.ganho_peso_view, name='ganho_peso'),
    path('ganho_peso/excluir/<int:pk>/', views.excluir_ganho, name='excluir_ganho'),
    path('ganho_peso/enviar_email/<int:pk>/', views.enviar_email_ganho, name='enviar_email_ganho'),
    path('mapa/', views.mapa_view, name='mapa'),
    path('formacaobebe/', views.formacaobebe, name='formacaobebe'),
    path('calculadora/', views.calcular_dpp, name='calculadora_dpp'),
    path('enviar_email_dpp/<int:pk>/', views.enviar_email_dpp, name='enviar_email_dpp'),
    path('buscar-livros/', views.buscar_livros, name='buscar_livros'),

    # Fórum
    path('forum/', views.forum, name='forum'),
    path('deletar-topico/<int:topico_id>/', views.deletar_topico, name='deletar_topico'),
    path('topico/<int:topico_id>/', views.detalhes_topico, name='detalhes_topico'),
    path('comentar/<int:topico_id>/', views.comentar_topico, name='comentar_topico'),
    path('deletar-comentario/<int:comentario_id>/', views.deletar_comentario, name='deletar_comentario'),
    path('curtir/<str:tipo>/<int:id_conteudo>/', views.curtir_conteudo, name='curtir_conteudo'), 
    path('reportar/<str:tipo>/<int:id_conteudo>/', views.reportar_conteudo, name='reportar_conteudo'),
    path('moderador/relatorios/', views.ver_relatorios, name='ver_relatorios'),
    path('excluir_relatorio/<int:relatorio_id>/', views.excluir_relatorio, name='excluir_relatorio'),

    # API
    path("api/", include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)