from django.db import models
from django.contrib.auth.models import User
from utilidades.models import FechasMixin

class Pregunta(FechasMixin):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    vistas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = "preguntas"
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"


class Respuesta(FechasMixin):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    votos_positivos = models.IntegerField(default=0)
    votos_negativos = models.IntegerField(default=0)

    def __str__(self):
        return f"Respuesta de {self.usuario.username} para la pregunta: {self.pregunta.titulo}"

    class Meta:
        db_table = "respuestas"
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"
