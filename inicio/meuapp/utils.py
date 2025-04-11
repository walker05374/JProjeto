from googleapiclient.discovery import build
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from geopy.distance import geodesic
import math
import requests
from django.conf import settings
from urllib.parse import urlencode






GOOGLE_API_KEY = 'AIzaSyDzn1gNy0Zjh2JRwULVJ-ZtC9a9r9VHwsw'
GOOGLE_CSE_ID = '47069417be7bc44e8'

def google_custom_search(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    result = service.cse().list(q=query, cx=GOOGLE_CSE_ID).execute()
    return result.get('items', [])


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()


def calcular_distancia(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).kilometers


def gerar_pontos_radiais(lat, lng, raio_km=140, passo_km=50):
    pontos = []
    R = 6371  # Raio médio da Terra em km
    num_passos = int((raio_km * 2) / passo_km)

    for dx in range(-num_passos//2, num_passos//2 + 1):
        for dy in range(-num_passos//2, num_passos//2 + 1):
            offset_lat = (passo_km * dy) / R * (180 / math.pi)
            offset_lng = (passo_km * dx) / (R * math.cos(math.radians(lat))) * (180 / math.pi)
            nova_lat = lat + offset_lat
            nova_lng = lng + offset_lng
            pontos.append((nova_lat, nova_lng))

    return pontos


def busca_ampla_postos(lat, lng):
    key = settings.GOOGLE_MAPS_API_KEY

    termos_busca = [
        "SESMA", "SESMA Belém", "Sistema Único de Saúde", "SUS", "Atendimento SUS",
        "Posto de saúde SUS", "Hospital público", "Clínica pública", "UBS", "UBSF", "USF",
        "Centro de Saúde", "Unidade de Saúde", "Unidade de Pronto Atendimento", "UPA",
        "Policlínica", "Policlínica municipal", "Hospital Municipal", "AME", 
        "AME Atendimento Médico Especializado", "Ambulatório Médico Especializado",
        "Atendimento pré-natal", "Exames para gestantes", "Pré-natal", 
        "Clínica obstétrica", "Hospital maternidade", "Atendimento obstétrico SUS",
        "Exames obstétricos SUS", "Centro de referência da mulher", "Clínica da mulher",
        "Centro de atenção à gestante", "Posto de saúde", "Clínica da família",
        "Clínica comunitária", "Saúde da mulher", "Posto médico", 
        "Hospital para exames", "Exames médicos gratuitos", 
        "Consultório público", "Centro médico público"
    ]

    pontos = gerar_pontos_radiais(lat, lng)
    resultados_unicos = {}

    termos_destaque = ["sesma", "sus", "ame", "maternidade", "gestante", "obstetr", "mulher"]

    for termo in termos_busca:
        for ponto_lat, ponto_lng in pontos:
            params = {
                "query": termo,
                "location": f"{ponto_lat},{ponto_lng}",
                "radius": 50000,
                "key": key
            }
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?{urlencode(params)}"

            response = requests.get(url)
            if response.status_code != 200:
                continue

            data = response.json()

            for result in data.get("results", []):
                place_id = result.get("place_id")
                nome_lower = result.get("name", "").lower()

                if place_id not in resultados_unicos:
                    resultados_unicos[place_id] = result

                # Garante que entradas importantes apareçam
                elif any(kw in nome_lower for kw in termos_destaque):
                    resultados_unicos[place_id] = result

    return list(resultados_unicos.values())

