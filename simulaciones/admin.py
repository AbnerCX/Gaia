from django.contrib import admin
from .models import Simulacion, CondicionesAmbientales, RecomendacionesCultivo


@admin.register(Simulacion)
class SimulacionAdmin(admin.ModelAdmin):
    list_display = ('campo', 'usuario','cultivo', 'condiciones', 'resultado_esperado')
    search_fields = ('campo__nombre', 'usuario__username', 'cultivo__nombre')
    list_filter = ('campo', 'cultivo', 'usuario','condiciones__fertilizante')
    autocomplete_fields = ['campo', 'cultivo', 'condiciones']

@admin.register(CondicionesAmbientales)
class CondicionesAmbientalesAdmin(admin.ModelAdmin):
    list_display = ('temperatura', 'humedad', 'precipitacion', 'viento', 'ph_agua', 'fertilizante')
    search_fields = ('temperatura', 'humedad', 'precipitacion')
    list_filter = ('fertilizante',)
    autocomplete_fields = ['fertilizante']

@admin.register(RecomendacionesCultivo)
class RecomendacionesCultivoAdmin(admin.ModelAdmin):
    list_display = ('cultivo', 'temperatura_min', 'temperatura_max', 'humedad_min', 'humedad_max')
    search_fields = ('cultivo__nombre',)
    list_filter = ('cultivo',)
    autocomplete_fields = ['cultivo']