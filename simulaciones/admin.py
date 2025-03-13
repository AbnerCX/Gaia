from django.contrib import admin
from .models import Simulacion, ValoresOptimos

@admin.register(ValoresOptimos)
class ValoresOptimosAdmin(admin.ModelAdmin):
    list_display = ('tipo_cultivo', 'humedad_minima', 'humedad_maxima', 'temperatura_minima', 'temperatura_maxima', 'precipitacion_minima', 'precipitacion_maxima')
    search_fields = ('tipo_cultivo__nombre',) 

@admin.register(Simulacion)
class SimulacionAdmin(admin.ModelAdmin):
    list_display = ('cultivo', 'usuario', 'campo', 'humedad_ingresada', 'temperatura_ingresada', 'precipitacion_ingresada', 'es_optimo')  
    
    # Para mostrar el nombre del tipo de cultivo en lugar del objeto completo
    def get_tipo_cultivo(self, obj):
        return obj.cultivo.tipo_cultivo.nombre
    get_tipo_cultivo.short_description = 'Tipo de Cultivo'

    # Asegúrate de que 'get_tipo_cultivo' se muestre en la lista
    list_display = ('get_tipo_cultivo', 'usuario', 'campo', 'humedad_ingresada', 'temperatura_ingresada', 'precipitacion_ingresada', 'es_optimo')

    search_fields = ('cultivo__tipo_cultivo__nombre', 'campo__nombre', 'usuario__username')


