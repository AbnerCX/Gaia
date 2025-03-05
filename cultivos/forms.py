from django import forms
from .models import Campo, Cultivo

class CampoForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['nombre', 'latitud', 'longitud', 'tamano']

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)  
        super(CampoForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.usuario = user 


class CultivoForm(forms.ModelForm):
    class Meta:
        model = Cultivo
        fields = ['campo', 'nombre', 'tipo_suelo', 'temporada_ideal', 'requerimentos']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extraer el usuario de kwargs
        super(CultivoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['campo'].queryset = Campo.objects.filter(usuario=user)