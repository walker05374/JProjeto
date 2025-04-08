from django.contrib import admin
from inicio.meuapp import models
from .models import Cliente,ContactMe,CustomUser,Vacina,Exame



from django.contrib.auth import get_user_model


User = get_user_model()


admin.site.register(Cliente)
admin.site.register(models.ContactMe)
admin.site.register(CustomUser)
admin.site.register(Vacina)
admin.site.register(Exame) 