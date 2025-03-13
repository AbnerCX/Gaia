from django.urls import path
from . import views

urlpatterns = [
    path('crear_simulacion/', views.realizar_simulacion, name='realizar_simulacion'),
    

]
