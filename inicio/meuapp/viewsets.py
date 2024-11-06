from rest_framework import viewsets
from .serializers import ClienteSerializer#GestanteSerializer
from .models import Cliente #Gestante

class ClienteViewSet(viewsets.ModelViewSet):
    model = Cliente
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
    filter_fields = ('nome','datanascimento','cpf','idadecrianca',
                  'sus','endereco','bairro','cep','cidade','uf','nomecrianca','generocrianca')
    

#class GestanteViewSet(viewsets.ModelViewSet):
  #  model = Gestante
    #serializer_class = GestanteSerializer
   # queryset = Gestante.objects.all()
    #filter_fields = ('usuario', 'datavacina', 'nome_vacina', 'status')