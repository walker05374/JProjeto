from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .viewsets import ClienteViewSet
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import verify_email  # Verifique o caminho correto para a função

router = routers.DefaultRouter()
router.register(r'cliente', ClienteViewSet, basename="Cliente")

urlpatterns = [
    path('', views.site, name='site'),
    path('vacina/', views.vacina, name='vacina'),
    path('prenatal/', views.prenatal, name='prenatal'),
    path('informacoes/', views.informacoes, name='informacoes'),
    path('mais/', views.mais, name='mais'),
    path('amamentacao/', views.amamentacao, name='amamentacao'),
    path('noticias/', views.noticias, name='noticias'),
    path('search/', views.search_results, name='search_results'),
    path('menu', views.menu, name='menu'),

    path('cep', views.cep, name='cep'),
    path("api/", include(router.urls)),

    path('verify_email/<int:pk>/', verify_email, name='verify_email'),



    path('create_cliente', views.create_cliente, name='create_cliente'),
    path('read_cliente', views.read_cliente, name='read_cliente'),
    path("update_cliente/<int:id>", views.update_cliente, name='update_cliente'),
    path("delete_cliente/<int:id>", views.delete_cliente, name='delete_cliente'),



    path('contact', views.contact_me, name='contact'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),





]







