from .models import Cliente #Gestante
from rest_framework import serializers


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nome','datanascimento','cpf','idadecrianca',
                  'sus','endereco','bairro','cep','cidade','uf','nomecrianca','generocrianca',]
        

        
        
#class GestanteSerializer(serializers.ModelSerializer): 
    #class Meta:
      #  model = Gestante
      #  filds = ['usuario', 'datavacina', 'nome_vacina', 'status']  
