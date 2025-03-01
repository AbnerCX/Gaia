from django.contrib import admin
from .models import Campo, Cultivo, Plagas, Fertilizantes, Pesticidas

@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud', 'tamano', 'creado', 'ultima_actualizacion')
    search_fields = ('nombre',)
    list_filter = ('creado', 'ultima_actualizacion')

@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_suelo', 'temporada_ideal') 
    search_fields = ('nombre',)

@admin.register(Plagas)
class PlagasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cultivo', 'creado', 'ultima_actualizacion')
    search_fields = ('nombre', 'cultivo__nombre')
    list_filter = ('cultivo', 'creado', 'ultima_actualizacion')

@admin.register(Pesticidas)
class PesticidasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'dosis', 'cultivo', 'creado', 'ultima_actualizacion')
    search_fields = ('nombre', 'cultivo__nombre')
    list_filter = ('cultivo', 'tipo', 'creado', 'ultima_actualizacion')

@admin.register(Fertilizantes)
class FertilizantesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'dosis', 'cultivo', 'creado', 'ultima_actualizacion')
    search_fields = ('nombre', 'cultivo__nombre')
    list_filter = ('cultivo', 'tipo', 'creado', 'ultima_actualizacion')