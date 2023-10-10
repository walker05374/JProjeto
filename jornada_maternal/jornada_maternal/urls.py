from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import (admin)
from allauth.socialaccount import providers
from django.shortcuts import redirect
from allauth.account.views import LoginView, LogoutView, SignupView 





urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path('', include('meuapp.urls')),
    path('accounts/', include('allauth.urls')),
    
   
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
]


