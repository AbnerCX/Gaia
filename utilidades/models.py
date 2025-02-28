from django.db import models

class FechasMixin(models.Model):
    creado = models.DateTimeField(auto_now_add=True, db_index=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True