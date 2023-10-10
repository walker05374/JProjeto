
import os

from django.core.asgi import get_asgi_application
from dj_static import Cling, MediaCling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jornada_maternal.settings')

application = Cling(MediaCling(get_asgi_application()))