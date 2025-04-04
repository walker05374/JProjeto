from django.contrib import admin
from django.urls import path, include
from . import views 
from rest_framework import routers
from .viewsets import ClienteViewSet
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from .views import verify_email
from inicio.meuapp import views as v
from django.conf import settings
from django.conf.urls.static import static

from .views import excluir_conta

from .views import MyPasswordReset

router = routers.DefaultRouter()

router.register(r'cliente', ClienteViewSet, basename="Cliente")




urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.site, name='site'),
    path('prenatal/', views.prenatal, name='prenatal'),
    path('informacoes/', views.informacoes, name='informacoes'),
    path('mais/', views.mais, name='mais'),
    path('amamentacao/', views.amamentacao, name='amamentacao'),
    path('noticias/', views.noticias, name='noticias'),
    path('search/', views.search_results, name='search_results'),
    path('menu', views.menu, name='menu'),

    path('cep', views.cep, name='cep'),
    path("api/", include(router.urls)),




    path('create_cliente', views.create_cliente, name='create_cliente'),
    path('read_cliente', views.read_cliente, name='read_cliente'),
    path("update_cliente/<int:id>", views.update_cliente, name='update_cliente'),
    path("delete_cliente/<int:id>", views.delete_cliente, name='delete_cliente'),
  

    path('verify_email/<int:pk>/', verify_email, name='verify_email'),
    path('contact', views.contact_me, name='contact'),






    path('reset-password/', MyPasswordReset.as_view(), name='password_reset'),



    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('account_activation_email/', LoginView.as_view(), name='account_activation_email'),  # noqa E501

    path('login/', LoginView.as_view(), name='login'),  # noqa E501
    path('logout/', LogoutView.as_view(), name='logout'),  # noqa E501
    path('update_profile/', views.update_profile, name='update_profile'),



    path('registro/', views.registro, name='registro'),
    path('reset/<uidb64>/<token>/', v.MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),  # noqa E501
    path('reset/done/', v.MyPasswordResetComplete.as_view(), name='password_reset_complete'),  # noqa E501
    path('excluir-conta/', excluir_conta, name='excluir-conta'),
    

    path("create_vacina", views.create_vacina, name="create_vacina"),
    path("read_vacina", views.read_vacina, name="read_vacina"),
    path("update_vacina/<int:id>", views.update_vacina, name="update_vacina"),
    path("delete_vacina/<int:id>", views.delete_vacina, name="delete_vacina"),




]

    
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
