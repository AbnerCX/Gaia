from django.shortcuts import render, get_object_or_404
from .models import Simulacion, Cultivo, Campo, ValoresOptimos
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def realizar_simulacion(request):
    # Obtener los campos y cultivos del usuario autenticado
    campos = Campo.objects.filter(usuario=request.user)
    cultivos = Cultivo.objects.filter(campo__in=campos)  # Solo los cultivos del usuario

    if request.method == "POST":
        cultivo_id = request.POST.get("cultivo")
        campo_id = request.POST.get("campo")
        humedad = request.POST.get("humedad")
        temperatura = request.POST.get("temperatura")
        precipitacion = request.POST.get("precipitacion")

        # Verificar que los campos no estén vacíos
        if not all([humedad, temperatura, precipitacion, cultivo_id, campo_id]):
            # Mostrar un mensaje de error si faltan campos
            return render(request, "formulario_simulacion.html", {"campos": campos, "cultivos": cultivos, "error": "Todos los campos son obligatorios."})

        # Obtener el cultivo y el campo correspondientes
        cultivo = get_object_or_404(Cultivo, id=cultivo_id, campo__usuario=request.user)
        campo = get_object_or_404(Campo, id=campo_id, usuario=request.user)

        # Crear la simulación
        simulacion = Simulacion.objects.create(
            usuario=request.user, 
            cultivo=cultivo,
            campo=campo,
            humedad_ingresada=humedad,
            temperatura_ingresada=temperatura,
            precipitacion_ingresada=precipitacion
        )

        # Evaluar si los valores ingresados son óptimos
        es_optimo = simulacion.evaluar_simulacion()

        return render(request, "resultado_simulacion.html", {"simulacion": simulacion, "es_optimo": es_optimo})

    return render(request, "formulario_simulacion.html", {"campos": campos, "cultivos": cultivos})
