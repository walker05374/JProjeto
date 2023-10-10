from .models import Cliente
#from .models import User
from rest_framework import serializers

#class UserSerializer(serializers.ModelSerializer):

    #class Meta:
       # model = User
        #fields = ['__all__']


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nome','datanascimento','cpf','idadecrianca',
                  'sus','endereco','bairro','cep','cidade','uf','nomecrianca','generocrianca',]