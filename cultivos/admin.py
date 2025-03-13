from django.contrib import admin
from .models import Campo, Cultivo, Plagas, Fertilizantes, Pesticidas, PlanificacionCultivo, TipoCultivo

@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'latitud', 'longitud', 'tamano', 'creado', 'ultima_actualizacion')
    search_fields = ('nombre', 'usuario__username')
    list_filter = ('creado', 'ultima_actualizacion')

@admin.register(TipoCultivo)
class TipoCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Asegúrate de mostrar los campos que quieres ver
    search_fields = ('nombre',)  # Permitir buscar por el nombre del tipo de cultivo

@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_cultivo_nombre', 'campo', 'tipo_suelo', 'temporada_ideal')  # Usar el método para obtener el nombre del tipo de cultivo
    list_filter = ("tipo_suelo", "temporada_ideal", "campo")
    search_fields = ('tipo_cultivo__nombre', 'campo__nombre')

    # Método para obtener el nombre del tipo de cultivo
    def get_tipo_cultivo_nombre(self, obj):
        return obj.tipo_cultivo.nombre
    get_tipo_cultivo_nombre.admin_order_field = 'tipo_cultivo'  # Permitir ordenar por este campo
    get_tipo_cultivo_nombre.short_description = 'Tipo de Cultivo'  # Nombre que aparecerá en la lista


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
    list_display = ('nombre', 'tipo', 'dosis', 'campo', 'creado', 'ultima_actualizacion')  
    search_fields = ('nombre', 'campo__nombre')  
    list_filter = ('campo', 'tipo', 'creado', 'ultima_actualizacion')  


@admin.register(Fertilizantes)
class FertilizantesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'dosis', 'campo', 'creado', 'ultima_actualizacion') 
    search_fields = ('nombre', 'campo__nombre') 
    list_filter = ('campo', 'tipo', 'creado', 'ultima_actualizacion') 
