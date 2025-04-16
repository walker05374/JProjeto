from .models import Cliente
from .models import Vacina





def vacina_context(request):
    if request.user.is_authenticated:
        tem_vacina = Vacina.objects.filter(usuario=request.user).exists()
    else:
        tem_vacina = False
    return {'tem_vacina': tem_vacina}

def clientes_context(request):
    """
    Verifica se o usuário tem clientes cadastrados e retorna uma variável booleana
    para ser usada globalmente nos templates.
    """
    if request.user.is_authenticated:
        # Verifica se o usuário tem um cliente cadastrado
        cliente = Cliente.objects.filter(user=request.user).first()
        return {'clientes_cadastrados': bool(cliente)}
        return {'clientes_cadastrados': Cliente.objects.exists()}
    return {'clientes_cadastrados': False}