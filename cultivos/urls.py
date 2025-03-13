
from django.urls import path
from django.contrib.auth.views import LogoutView 
from .views import home, registrarse, login_vista, admin_campos, admin_cultivos
from .views import admin_plagas, admin_planificaciones, admin_pesticidas, admin_fertilizantes


urlpatterns = [
    path('', home, name='home'),
    path('registrarse/', registrarse, name='registrarse'),
    path('login/', login_vista, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('admin_campos/', admin_campos, name='admin_campos'),
    path('admin_cultivos/', admin_cultivos, name='admin_cultivos'),
    path('admin_plagas/', admin_plagas, name='admin_plagas'),
    path('admin_planificaciones/', admin_planificaciones, name='admin_planificaciones'),
    path('admin_pesticidas/', admin_pesticidas, name='admin_pesticidas'),
    path('admin_fertilizantes/', admin_fertilizantes, name='admin_fertilizantes'),
    
]