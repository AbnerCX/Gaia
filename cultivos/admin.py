from django.contrib import admin
from .models import Campo, Cultivo, Plagas, Fertilizantes, Pesticidas, PlanificacionCultivo

@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario','latitud', 'longitud', 'tamano', 'creado', 'ultima_actualizacion')
    search_fields = ('nombre', 'usuario__username')
    list_filter = ('creado', 'ultima_actualizacion')

@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'campo', 'tipo_suelo', 'temporada_ideal') 
    list_filter = ("tipo_suelo", "temporada_ideal", "campo")
    search_fields = ('nombre','campo__nombre')

@admin.register(PlanificacionCultivo)
class PlanificacionCultivoAdmin(admin.ModelAdmin):
    list_display = ("cultivo", "campo", "fecha_plantacion", "fecha_cosecha", "estado")
    list_filter = ("estado", "campo", "cultivo")
    search_fields = ("cultivo__nombre", "campo__nombre")
    ordering = ("fecha_plantacion",)

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