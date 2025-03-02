from django.db import models

class FechasMixin(models.Model):
    creado = models.DateTimeField(auto_now_add=True, db_index=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

class Productos(models.Model):
    FRECUENCIA_CHOICES = [
        (1, "Diario"),
        (2, "Semanal"),
        (3, "Mensual"),
        (4, "Trimestral"),
        (5, "Anual"),
    ]
    
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20)
    dosis = models.DecimalField(max_digits=5, decimal_places=2)
    frecuencia = models.IntegerField(choices=FRECUENCIA_CHOICES)

    class Meta:
        abstract = True