from django.urls import path
from . import views

urlpatterns = [
    path('lista_preguntas/', views.lista_preguntas, name='lista_preguntas'),  # Agregar barra inclinada al final
    path('pregunta/<int:pk>/', views.detalle_pregunta, name='detalle_pregunta'),
    path('pregunta/nueva/', views.nueva_pregunta, name='nueva_pregunta'),
]
