from django.db import models
from django.contrib.auth.models import User
from utilidades.models import FechasMixin, Productos

class Campo(FechasMixin):  
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)  
    longitud = models.DecimalField(max_digits=10, decimal_places=6) 
    tamano = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="tamaño")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        db_table = "campos"
        verbose_name = "Campo"
        verbose_name_plural = "Campos"

class TipoCultivo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "tipos_cultivo"
        verbose_name = "Tipo de Cultivo"
        verbose_name_plural = "Tipos de Cultivo"

class Cultivo(FechasMixin):

    class TipoDeSuelo(models.IntegerChoices):
        ARCILLOSO = 1, "Arcilloso"
        ARENOSO = 2, "Arenoso"
        LIMOSO = 3, "Limoso"
        FRANCO = 4, "Franco"
        PEDREGOSO = 5, "Pedregoso"

    class TemporadaIdeal(models.IntegerChoices):
        PRIMAVERA = 1, "Primavera"
        VERANO = 2, "Verano"
        OTONO = 3, "Otoño"
        INVIERNO = 4, "Invierno"
    
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    tipo_cultivo = models.ForeignKey(TipoCultivo, on_delete=models.CASCADE)
    tipo_suelo = models.IntegerField(choices=TipoDeSuelo.choices)
    temporada_ideal = models.IntegerField(choices=TemporadaIdeal.choices)
    requerimentos = models.TextField()

    def __str__(self):
        return f"{self.tipo_cultivo.nombre} - {self.get_tipo_suelo_display()} - {self.get_temporada_ideal_display()}"

    class Meta:
        db_table = "cultivos"
        verbose_name = "Cultivo"
        verbose_name_plural = "Cultivos"

class PlanificacionCultivo(FechasMixin):

    class EstadoPlanificacion(models.IntegerChoices):
        PENDIENTE = 1, "Pendiente"
        EN_PROCESO = 2, "En proceso"
        COMPLETADA = 3, "Completada"
        CANCELADA = 4, "Cancelada"

    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    fecha_plantacion = models.DateField()
    fecha_cosecha = models.DateField()
    cantidad_semillas = models.PositiveIntegerField()
    rendimiento_esperado = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.IntegerField(choices=EstadoPlanificacion.choices, default=EstadoPlanificacion.PENDIENTE)

    def planificar_cultivo(self):
        if self.fecha_cosecha <= self.fecha_plantacion:
            raise ValueError("La fecha de cosecha debe ser posterior a la fecha de plantacion.")
        
        return f"Planificacion de {self.cultivo.nombre} en {self.campo.nombre} programada del {self.fecha_plantacion} al {self.fecha_cosecha}."

    def __str__(self):
        return f"Planificacion de {self.cultivo.nombre} en {self.campo.nombre} ({self.get_estado_display()})"

    class Meta:
        db_table = "planificacion_cultivo"
        verbose_name = "Planificacion de Cultivo"
        verbose_name_plural = "Planificaciones de Cultivos"


class Plagas(FechasMixin):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    efectos = models.TextField()
    tratamiento = models.TextField()

    def __str__(self):
        return f"{self.nombre} en {self.cultivo.nombre}"
    
    class Meta:
        db_table = "plagas"
        verbose_name = "Plaga"
        verbose_name_plural = "Plagas"

class Pesticidas(FechasMixin, Productos):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)  # Relación con Campo

    def __str__(self):
        return f"{self.nombre} - ({self.tipo} para el campo {self.campo.nombre})"  # Actualizado para mostrar el campo
    
    class Meta:
        db_table = "pesticida"
        verbose_name = "Pesticida"
        verbose_name_plural = "Pesticidas"

class Fertilizantes(FechasMixin, Productos):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)  # Relación con Campo

    def __str__(self):
        return f"{self.nombre} - ({self.tipo} para el campo {self.campo.nombre})"  # Actualizado para mostrar el campo
    
    class Meta:
        db_table = "fertilizante"
        verbose_name = "Fertilizante"
        verbose_name_plural = "Fertilizantes"



