from django.contrib import admin
from .models import Simulacion, CondicionesAmbientales


@admin.register(CondicionesAmbientales)
class CondicionesAmbientalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperatura', 'humedad', 'precipitacion', 'viento', 'ph_agua', 'fertilizante', 'creado')
    list_filter = ('temperatura', 'humedad', 'ph_agua', 'fertilizante')
    search_fields = ('temperatura', 'humedad', 'ph_agua')

@admin.register(Simulacion)
class SimulacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'campo', 'cultivo', 'condiciones', 'resultado_esperado', 'creado', 'ultima_actualizacion')
    list_filter = ('campo', 'cultivo', 'condiciones')
    search_fields = ('campo__nombre', 'cultivo__nombre', 'condiciones__temperatura', 'condiciones__humedad')