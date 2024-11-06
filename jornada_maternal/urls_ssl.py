from django.urls import url
from django.http import HttpResponse

urlpatterns = [
    url(r'^', lambda request: HttpResponse(status=204), name='ssl-noop'),
]
