from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cliente, ContactMe, CustomUser, Vacina, Topico  

# Registrando CustomUserAdmin para CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']


class TopicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'data_criacao', 'ativo']  # Exibindo os campos desejados no painel de administração
    search_fields = ['titulo', 'usuario__username']  # Permitindo buscar pelo título ou nome do usuário
    list_filter = ['ativo', 'data_criacao']  # Permitindo filtrar tópicos por status e data


# Registrando o CustomUser e associando ao CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Cliente)
admin.site.register(ContactMe)
admin.site.register(Vacina)
admin.site.register(Topico, TopicoAdmin)  
