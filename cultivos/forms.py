from django import forms
from .models import Campo, Cultivo, Plagas, PlanificacionCultivo
from .models import Pesticidas, Fertilizantes

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

class PlagasForm(forms.ModelForm):
    class Meta:
        model = Plagas
        fields = ['cultivo', 'nombre', 'efectos', 'tratamiento']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extraer el usuario de kwargs
        super(PlagasForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['cultivo'].queryset = Cultivo.objects.filter(campo__usuario=user)

class PlanificacionCultivoForm(forms.ModelForm):
    class Meta:
        model = PlanificacionCultivo
        fields = ['campo', 'cultivo', 'fecha_plantacion', 'fecha_cosecha', 'cantidad_semillas', 'rendimiento_esperado', 'estado']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extraer el usuario de kwargs
        super(PlanificacionCultivoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['campo'].queryset = Campo.objects.filter(usuario=user)
            self.fields['cultivo'].queryset = Cultivo.objects.filter(campo__usuario=user)

        self.fields['fecha_plantacion'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['fecha_cosecha'].widget = forms.DateInput(attrs={'type': 'date'})

class PesticidaForm(forms.ModelForm):
    class Meta:
        model = Pesticidas
        fields = ['nombre', 'tipo', 'dosis', 'frecuencia', 'cultivo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PesticidaForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['cultivo'].queryset = user.cultivo_set.all()

class FertilizanteForm(forms.ModelForm):
    class Meta:
        model = Fertilizantes
        fields = ['nombre', 'tipo', 'dosis', 'frecuencia', 'cultivo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FertilizanteForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['cultivo'].queryset = user.cultivo_set.all() 