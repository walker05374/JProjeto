# accounts/services.py
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
import googlemaps
from django.conf import settings
from .models import PostoSaude

def send_mail_to_user(request, user):
    current_site = get_current_site(request)
    use_https = request.is_secure()
    subject = 'Ative sua conta.'
    message = render_to_string('email/account_activation_email.html', {
        'user': user,
        'protocol': 'https' if use_https else 'http',
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)



gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def buscar_postos_por_localizacao(latitude, longitude, radius=5000):
    places_result = gmaps.places_nearby(location=(latitude, longitude), radius=radius, type='hospital')
    postos = []
    for place in places_result['results']:
        posto, created = PostoSaude.objects.get_or_create(
            nome=place['name'],
            endereco=place.get('vicinity', 'Endereço não disponível'),
            latitude=place['geometry']['location']['lat'],
            longitude=place['geometry']['location']['lng']
        )
        postos.append(posto)
    return postos