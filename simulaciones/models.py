from django.db import models
from cultivos.models import Campo, Cultivo, Fertilizantes
from utilidades.models import FechasMixin

class CondicionesAmbientales(FechasMixin):
    temperatura = models.DecimalField(max_digits=5, decimal_places=2) 
    humedad = models.DecimalField(max_digits=5, decimal_places=2)  
    precipitacion = models.DecimalField(max_digits=5, decimal_places=2)  
    viento = models.DecimalField(max_digits=5, decimal_places=2) 
    ph_agua = models.DecimalField(max_digits=3, decimal_places=1)  
    fertilizante = models.ForeignKey(Fertilizantes, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"T: {self.temperatura}°C, H: {self.humedad}%, pH: {self.ph_agua}"

    class Meta:
        db_table = "condiciones_ambientales"
        verbose_name = "Condiciones Ambientales"
        verbose_name_plural = "Condiciones Ambientales"


class Simulacion(FechasMixin):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    condiciones = models.ForeignKey(CondicionesAmbientales, on_delete=models.CASCADE)
    resultado_esperado = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Simulacion para {self.cultivo.nombre} en {self.campo.nombre}"

    class Meta:
        db_table = "simulaciones"
        verbose_name = "Simulacion"
        verbose_name_plural = "Simulaciones"
