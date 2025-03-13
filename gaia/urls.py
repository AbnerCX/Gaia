from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cultivos.urls')),
    path('simulacion/', include('simulaciones.urls')),
    path('foro/', include('foro.urls')),
]

