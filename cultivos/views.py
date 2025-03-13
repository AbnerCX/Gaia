from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Campo, Cultivo, Plagas, PlanificacionCultivo, Pesticidas, Fertilizantes
from .forms import CampoForm, CultivoForm, PlagasForm, PlanificacionCultivoForm, PesticidaForm, FertilizanteForm

def home(request):
    return render(request, 'home.html')

def registrarse(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registrarse.html', {'form': form})

def login_vista(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def admin_campos(request):
    editing = False
    campo_a_editar = None  # Almacenará el campo a editar, si lo hay
    campos = Campo.objects.filter(usuario=request.user)  # Solo mostrar campos del usuario actual

    # Si es una solicitud POST
    if request.method == 'POST':
        # Eliminar campo
        if 'eliminar_id' in request.POST:
            campo_id = request.POST.get('eliminar_id')
            campo = Campo.objects.get(id=campo_id, usuario=request.user)
            campo.delete()  # Elimina el campo
            return redirect('admin_campos')  # Redirige a la misma página después de eliminar

        # Si se está editando un campo
        elif 'campo_id' in request.POST:
            campo_id = request.POST.get('campo_id')
            campo_a_editar = Campo.objects.get(id=campo_id, usuario=request.user)
            form = CampoForm(request.POST, instance=campo_a_editar)
            if form.is_valid():
                form.save()  # Guarda los cambios en el campo editado
                return redirect('admin_campos')  # Redirige a la misma página después de guardar

            editing = True  # Activamos el modo edición

        # Si se está creando un nuevo campo
        else:
            form = CampoForm(request.POST)
            if form.is_valid():
                nuevo_campo = form.save(commit=False)
                nuevo_campo.usuario = request.user  # Asignamos el campo al usuario actual
                nuevo_campo.save()  # Guardamos el nuevo campo
                return redirect('admin_campos')  # Redirige a la misma página después de crear

    # Si es una solicitud GET o estamos en el modo normal de creación
    else:
        form = CampoForm()

    return render(request, 'admin_campos.html', {
        'campos': campos,
        'form': form,
        'editing': editing,
        'campo_a_editar': campo_a_editar,  # Pasamos el campo a editar, si es necesario
    })


@login_required(login_url='/login/')
def admin_cultivos(request):
    editing = False
    cultivo_a_editar = None  # Almacenará el cultivo a editar, si lo hay
    cultivos = Cultivo.objects.filter(campo__usuario=request.user)  # Solo mostrar cultivos del usuario actual

    # Si es una solicitud POST
    if request.method == 'POST':
        # Eliminar cultivo
        if 'eliminar_id' in request.POST:
            cultivo_id = request.POST.get('eliminar_id')
            cultivo = Cultivo.objects.get(id=cultivo_id, campo__usuario=request.user)
            cultivo.delete()  # Elimina el cultivo
            return redirect('admin_cultivos')  # Redirige a la misma página después de eliminar

        # Si se está editando un cultivo
        elif 'cultivo_id' in request.POST:
            cultivo_id = request.POST.get('cultivo_id')
            cultivo_a_editar = Cultivo.objects.get(id=cultivo_id, campo__usuario=request.user)
            form = CultivoForm(request.POST, instance=cultivo_a_editar, user=request.user)
            if form.is_valid():
                form.save()  # Guarda los cambios en el cultivo editado
                return redirect('admin_cultivos')  # Redirige a la misma página después de guardar

            editing = True  # Activamos el modo edición

        # Si se está creando un nuevo cultivo
        else:
            form = CultivoForm(request.POST, user=request.user)
            if form.is_valid():
                nuevo_cultivo = form.save(commit=False)
                nuevo_cultivo.save()  # Guardamos el nuevo cultivo
                return redirect('admin_cultivos')  # Redirige a la misma página después de crear

    # Si es una solicitud GET o estamos en el modo normal de creación
    else:
        form = CultivoForm(user=request.user)

    return render(request, 'admin_cultivos.html', {
        'cultivos': cultivos,
        'form': form,
        'editing': editing,
        'cultivo_a_editar': cultivo_a_editar,  # Pasamos el cultivo a editar, si es necesario
    })

@login_required(login_url='/login/')
def admin_plagas(request):
    editing = False
    plaga_a_editar = None
    # Filtrar las plagas del usuario, pero por campo, no por cultivo
    plagas = Plagas.objects.filter(cultivo__campo__usuario=request.user)  # Filtrar las plagas por campo

    # Si la solicitud es POST
    if request.method == 'POST':
        # Eliminar plaga
        if 'eliminar_plaga_id' in request.POST:
            plaga_id = request.POST.get('eliminar_plaga_id')
            plaga = Plagas.objects.get(id=plaga_id, cultivo__campo__usuario=request.user)
            plaga.delete()
            return redirect('admin_plagas')

        # Editar plaga
        elif 'plaga_id' in request.POST:
            plaga_id = request.POST.get('plaga_id')
            plaga_a_editar = Plagas.objects.get(id=plaga_id, cultivo__campo__usuario=request.user)
            form = PlagasForm(request.POST, instance=plaga_a_editar, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('admin_plagas')
            editing = True

        # Crear nueva plaga
        else:
            form = PlagasForm(request.POST, user=request.user)
            if form.is_valid():
                nueva_plaga = form.save(commit=False)
                nueva_plaga.save()
                return redirect('admin_plagas')

    else:
        form = PlagasForm(user=request.user)

    return render(request, 'admin_plagas.html', {
        'plagas': plagas,
        'form': form,
        'editing': editing,
        'plaga_a_editar': plaga_a_editar,  # Pasamos la plaga si estamos editando
    })


@login_required(login_url='/login/')
def admin_planificaciones(request):
    editing = False
    planificacion_a_editar = None

    # Obtener todas las planificaciones del usuario
    planificaciones = PlanificacionCultivo.objects.filter(campo__usuario=request.user)

    if request.method == 'POST':
        # Eliminar planificacion
        if 'eliminar_planificacion_id' in request.POST:
            planificacion_id = request.POST.get('eliminar_planificacion_id')
            planificacion = PlanificacionCultivo.objects.get(id=planificacion_id)
            planificacion.delete()
            return redirect('admin_planificaciones')

        # Editar planificación
        elif 'editar_planificacion_id' in request.POST:
            planificacion_id = request.POST.get('editar_planificacion_id')
            planificacion_a_editar = PlanificacionCultivo.objects.get(id=planificacion_id)
            form = PlanificacionCultivoForm(instance=planificacion_a_editar, user=request.user)
            editing = True

        else:
            if 'planificacion_id' in request.POST:
                planificacion_a_editar = PlanificacionCultivo.objects.get(id=request.POST.get('planificacion_id'))
                form = PlanificacionCultivoForm(request.POST, instance=planificacion_a_editar, user=request.user)
                editing = True
            else:
                form = PlanificacionCultivoForm(request.POST, user=request.user)

            if form.is_valid():
                form.save()
                return redirect('admin_planificaciones')

    # Si es una solicitud GET o estamos en el modo normal de creación
    if not planificacion_a_editar:
        form = PlanificacionCultivoForm(user=request.user)

    return render(request, 'admin_planificaciones.html', {
        'form': form,
        'planificaciones': planificaciones,  # Enviar planificaciones a la plantilla
        'editing': editing,
        'planificacion_a_editar': planificacion_a_editar,
    })

@login_required(login_url='/login/')
def admin_pesticidas(request):
    editing = False
    pesticida_a_editar = None

    if request.method == 'POST':
        # Eliminar pesticida
        if 'eliminar_pesticida_id' in request.POST:
            pesticida_id = request.POST.get('eliminar_pesticida_id')
            pesticida = Pesticidas.objects.get(id=pesticida_id)
            pesticida.delete()
            return redirect('admin_pesticidas')

        # Editar pesticida
        elif 'editar_pesticida_id' in request.POST:
            pesticida_id = request.POST.get('editar_pesticida_id')
            pesticida_a_editar = Pesticidas.objects.get(id=pesticida_id)
            form = PesticidaForm(instance=pesticida_a_editar, user=request.user)
            editing = True

        else:
            # Si no es una solicitud de edición, se crea o actualiza el pesticida
            if 'pesticida_id' in request.POST:
                pesticida_a_editar = Pesticidas.objects.get(id=request.POST.get('pesticida_id'))
                form = PesticidaForm(request.POST, instance=pesticida_a_editar, user=request.user)
                editing = True
            else:
                form = PesticidaForm(request.POST, user=request.user)

            if form.is_valid():
                form.save()
                return redirect('admin_pesticidas')

    # Si es una solicitud GET o estamos en el modo de crear
    if not pesticida_a_editar:
        form = PesticidaForm(user=request.user)

    # Obtener los pesticidas del usuario actual, filtrados por campo
    pesticidas = Pesticidas.objects.filter(campo__usuario=request.user)

    return render(request, 'admin_pesticidas.html', {
        'form': form,
        'pesticidas': pesticidas,
        'editing': editing,
        'pesticida_a_editar': pesticida_a_editar,
    })

@login_required(login_url='/login/')
def admin_fertilizantes(request):
    editing = False
    fertilizante_a_editar = None

    # Si es una solicitud POST, verificar si es para eliminar o editar
    if request.method == 'POST':
        # Eliminar fertilizante
        if 'eliminar_fertilizante_id' in request.POST:
            fertilizante_id = request.POST.get('eliminar_fertilizante_id')
            fertilizante = get_object_or_404(Fertilizantes, id=fertilizante_id)
            # Asegurarse que el fertilizante pertenece al campo del usuario
            if fertilizante.campo.usuario == request.user:
                fertilizante.delete()
            return redirect('admin_fertilizantes')

        # Editar fertilizante
        elif 'editar_fertilizante_id' in request.POST:
            fertilizante_id = request.POST.get('editar_fertilizante_id')
            fertilizante_a_editar = get_object_or_404(Fertilizantes, id=fertilizante_id)
            # Asegurarse que el fertilizante pertenece al campo del usuario
            if fertilizante_a_editar.campo.usuario == request.user:
                form = FertilizanteForm(instance=fertilizante_a_editar, user=request.user)
                editing = True
            else:
                return redirect('admin_fertilizantes')

        # Guardar cambios o crear nuevo fertilizante
        else:
            if 'fertilizante_id' in request.POST:
                fertilizante_a_editar = get_object_or_404(Fertilizantes, id=request.POST.get('fertilizante_id'))
                form = FertilizanteForm(request.POST, instance=fertilizante_a_editar, user=request.user)
                editing = True
            else:
                form = FertilizanteForm(request.POST, user=request.user)

            if form.is_valid():
                form.save()
                return redirect('admin_fertilizantes')

    # Si es una solicitud GET o estamos en el modo normal de creación
    if not fertilizante_a_editar:
        form = FertilizanteForm(user=request.user)

    # Obtener los fertilizantes que pertenecen al usuario
    fertilizantes = Fertilizantes.objects.filter(campo__usuario=request.user)

    return render(request, 'admin_fertilizantes.html', {
        'form': form,
        'fertilizantes': fertilizantes,
        'editing': editing,
        'fertilizante_a_editar': fertilizante_a_editar,
    })
