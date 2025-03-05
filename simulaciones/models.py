from django.db import models
from django.contrib.auth.models import User
from cultivos.models import Campo, Cultivo, Fertilizantes
from utilidades.models import FechasMixin

class RecomendacionesCultivo(FechasMixin):
    cultivo = models.OneToOneField(Cultivo, on_delete=models.CASCADE, related_name='recomendaciones')
    temperatura_min = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura_max = models.DecimalField(max_digits=5, decimal_places=2)
    humedad_min = models.DecimalField(max_digits=5, decimal_places=2)
    humedad_max = models.DecimalField(max_digits=5, decimal_places=2)
    precipitacion_min = models.DecimalField(max_digits=5, decimal_places=2)
    precipitacion_max = models.DecimalField(max_digits=5, decimal_places=2)
    viento_min = models.DecimalField(max_digits=5, decimal_places=2)
    viento_max = models.DecimalField(max_digits=5, decimal_places=2)
    ph_agua_min = models.DecimalField(max_digits=3, decimal_places=1)
    ph_agua_max = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f"Recomendaciones para {self.cultivo.get_nombre_display()}"

    class Meta:
        db_table = "recomendaciones_cultivo"
        verbose_name = "Recomendacion de Cultivo"
        verbose_name_plural = "Recomendaciones de Cultivos"

class CondicionesAmbientales(FechasMixin):
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    humedad = models.DecimalField(max_digits=5, decimal_places=2)
    precipitacion = models.DecimalField(max_digits=5, decimal_places=2)
    viento = models.DecimalField(max_digits=5, decimal_places=2)
    ph_agua = models.DecimalField(max_digits=3, decimal_places=1)
    fertilizante = models.ForeignKey(Fertilizantes, on_delete=models.SET_NULL, null=True, blank=True)

    def validar_condiciones(self, cultivo):
        recomendaciones = cultivo.recomendaciones
        resultados = []

        if not (recomendaciones.temperatura_min <= self.temperatura <= recomendaciones.temperatura_max):
            resultados.append(f"Temperatura fuera del rango recomendado ({recomendaciones.temperatura_min}-{recomendaciones.temperatura_max} °C).")
        
        if not (recomendaciones.humedad_min <= self.humedad <= recomendaciones.humedad_max):
            resultados.append(f"Humedad fuera del rango recomendado ({recomendaciones.humedad_min}-{recomendaciones.humedad_max} %).")
        
        if not (recomendaciones.precipitacion_min <= self.precipitacion <= recomendaciones.precipitacion_max):
            resultados.append(f"Precipitacion fuera del rango recomendado ({recomendaciones.precipitacion_min}-{recomendaciones.precipitacion_max} mm).")
        
        if not (recomendaciones.viento_min <= self.viento <= recomendaciones.viento_max):
            resultados.append(f"Viento fuera del rango recomendado ({recomendaciones.viento_min}-{recomendaciones.viento_max} km/h).")
        
        if not (recomendaciones.ph_agua_min <= self.ph_agua <= recomendaciones.ph_agua_max):
            resultados.append(f"pH del agua fuera del rango recomendado ({recomendaciones.ph_agua_min}-{recomendaciones.ph_agua_max}).")

        return resultados if resultados else "Las condiciones son optimas para el cultivo."

    def __str__(self):
        return f"T: {self.temperatura}°C, H: {self.humedad}%, pH: {self.ph_agua}"

    class Meta:
        db_table = "condiciones_ambientales"
        verbose_name = "Condiciones Ambientales"
        verbose_name_plural = "Condiciones Ambientales"

class Simulacion(FechasMixin):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
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
