from .models import Cliente
from .models import Vacina
def clientes_context(request):
    return {'clientes_cadastrados': Cliente.objects.exists()}



def vacina_context(request):
    if request.user.is_authenticated:
        tem_vacina = Vacina.objects.filter(usuario=request.user).exists()
    else:
        tem_vacina = False
    return {'tem_vacina': tem_vacina}
