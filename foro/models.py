from django.db import models
from django.contrib.auth.models import User
from utilidades.models import FechasMixin

class Pregunta(FechasMixin):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = "preguntas"
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"


class Respuesta(FechasMixin):
    contenido = models.TextField()
    pregunta = models.ForeignKey(Pregunta, related_name='respuestas', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Respuesta de {self.usuario.username}"

    class Meta:
        db_table = "respuestas"
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"
