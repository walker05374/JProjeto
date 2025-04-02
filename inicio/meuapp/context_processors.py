from .models import Cliente

def clientes_context(request):
    return {'clientes_cadastrados': Cliente.objects.exists()}
