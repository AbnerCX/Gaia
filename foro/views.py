from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Pregunta, Respuesta
from .forms import PreguntaForm, RespuestaForm

def lista_preguntas(request):
    preguntas = Pregunta.objects.all().order_by('-creado')
    return render(request, 'lista_preguntas.html', {'preguntas': preguntas})

def detalle_pregunta(request, pk):
    pregunta = get_object_or_404(Pregunta, pk=pk)  # Usamos pk (id)
    respuestas = pregunta.respuestas.all()
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.pregunta = pregunta
            respuesta.usuario = request.user
            respuesta.save()
            return redirect('detalle_pregunta', pk=pregunta.pk)  # Redirigimos con pk (id)
    else:
        form = RespuestaForm()
    return render(request, 'detalle_pregunta.html', {'pregunta': pregunta, 'respuestas': respuestas, 'form': form})

@login_required(login_url='/login/')
def nueva_pregunta(request):
    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.usuario = request.user
            pregunta.save()
            return redirect('detalle_pregunta', pk=pregunta.pk)  # Redirigimos con pk (id)
    else:
        form = PreguntaForm()
    return render(request, 'nueva_pregunta.html', {'form': form})
