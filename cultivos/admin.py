from django.contrib import admin
from .models import Campo, Cultivo

@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud', 'tamano', 'creado', 'ultima_actualizacion')
    search_fields = ('nombre',)
    list_filter = ('creado', 'ultima_actualizacion')

@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_suelo', 'temporada_ideal') 
    search_fields = ('nombre',)
