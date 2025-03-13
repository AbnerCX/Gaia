from django.db import models
from django.contrib.auth.models import User
from cultivos.models import TipoCultivo,Cultivo, Campo
from decimal import Decimal

class ValoresOptimos(models.Model):
    tipo_cultivo = models.ForeignKey(TipoCultivo, on_delete=models.CASCADE)  # Relacionar con TipoCultivo
    humedad_minima = models.DecimalField(max_digits=5, decimal_places=2)
    humedad_maxima = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura_minima = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura_maxima = models.DecimalField(max_digits=5, decimal_places=2)
    precipitacion_minima = models.DecimalField(max_digits=5, decimal_places=2)
    precipitacion_maxima = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "valores_optimos"
        verbose_name = "Valores optimos"
        verbose_name_plural = "Valores optimos"

    def __str__(self):
        return f"Valores optimos para {self.tipo_cultivo.nombre}"  # Cambiar a tipo_cultivo


class Simulacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    humedad_ingresada = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura_ingresada = models.DecimalField(max_digits=5, decimal_places=2)
    precipitacion_ingresada = models.DecimalField(max_digits=5, decimal_places=2)
    es_optimo = models.BooleanField(default=False)  # Agregar el campo es_optimo

    def evaluar_simulacion(self):
        try:
            # Recuperamos los valores óptimos para el tipo de cultivo
            valores_optimos = ValoresOptimos.objects.get(tipo_cultivo=self.cultivo.tipo_cultivo)
        except ValoresOptimos.DoesNotExist:
            self.es_optimo = False
            self.save()
            return False  # Si no se encuentran los valores óptimos, retornamos False

        # Verificar que los valores ingresados sean válidos
        try:
            humedad = Decimal(self.humedad_ingresada)
            temperatura = Decimal(self.temperatura_ingresada)
            precipitacion = Decimal(self.precipitacion_ingresada)
        except (ValueError, TypeError) as e:
            self.es_optimo = False
            self.save()
            return False  # Si hay error en la conversión, devolvemos False
        
        es_optimo = (valores_optimos.humedad_minima <= humedad <= valores_optimos.humedad_maxima and
                     valores_optimos.temperatura_minima <= temperatura <= valores_optimos.temperatura_maxima and
                     valores_optimos.precipitacion_minima <= precipitacion <= valores_optimos.precipitacion_maxima)
        
        # Guardamos el resultado
        self.es_optimo = es_optimo
        self.save()
        
        return es_optimo

    class Meta:
        db_table = "simulaciones"
        verbose_name = "Simulacion"
        verbose_name_plural = "Simulaciones"

    def __str__(self):

        return f"Simulacion en {self.campo.nombre} para {self.cultivo.tipo_cultivo.nombre}"

