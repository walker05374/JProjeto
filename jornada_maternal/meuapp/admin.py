from django.contrib import admin
from meuapp import models
from .models import Cliente
from django.contrib.auth.models import User
from django.contrib.auth import forms


admin.site.register(Cliente)
admin.site.register(models.ContactMe)



# Register your models here.
class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = forms.UserCreationForm.Meta.fields + ('email','first_name','last_name',)
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'
            