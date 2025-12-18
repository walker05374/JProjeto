from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import (admin)
from allauth.socialaccount import providers
from django.shortcuts import redirect
from allauth.account.views import LoginView, LogoutView, SignupView 
from django.conf import settings

from django.http import HttpResponse


from django.views.generic import TemplateView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path('', include('inicio.meuapp.urls')),
    path('', include('allauth.urls')),
    path('', lambda x: HttpResponse('')),
    
    
   
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='ogout'),
    path('register/', SignupView.as_view(), name='register'),
    path('oauth/', include('social_django.urls', namespace='social')),

    


    # ---PWA ---
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw.js'),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest.json'),
]


if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 