from django.db import models
from utilidades.models import FechasMixin, Productos

class Campo(FechasMixin):  
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

class Cultivo(FechasMixin):
    
    TIPO_DE_SUELO_CHOICES = [
        (1, "Arcilloso"),
        (2, "Arenoso"),
        (3, "Limoso"),
        (4, "Franco"),
        (5, "Pedregoso"),
    ]
    
    TEMPORADA_IDEAL_CHOICES = [
        (1, "Primavera"),
        (2, "Verano"),
        (3, "Otoño"),
        (4, "Invierno"), 
    ]
    
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    tipo_suelo = models.IntegerField(choices=TIPO_DE_SUELO_CHOICES)
    temporada_ideal = models.IntegerField(choices=TEMPORADA_IDEAL_CHOICES)
    requerimentos = models.TextField()
 


    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_suelo_display()} - {self.get_temporada_ideal_display()}"
    
    class Meta:
        db_table = "cultivos"
        verbose_name = "Cultivo"
        verbose_name_plural = "Cultivos"

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
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - ({self.tipo} para {self.cultivo.nombre})"
    
    class Meta:
        db_table = "pesticida"
        verbose_name = "Pesticida"
        verbose_name_plural = "Pesticidas"

class Fertilizantes(FechasMixin, Productos):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - ({self.tipo} para {self.cultivo.nombre})"
    
    class Meta:
        db_table = "fertilizante"
        verbose_name = "Fertilizante"
        verbose_name_plural = "Fertilizantes"