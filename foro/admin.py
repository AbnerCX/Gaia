from django.contrib import admin
from .models import Pregunta, Respuesta

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'creado')
    search_fields = ('titulo', 'contenido', 'usuario__username')

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'usuario', 'creado')
    search_fields = ('contenido', 'usuario__username')
