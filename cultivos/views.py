from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Campo, Cultivo, Plagas,PlanificacionCultivo, Pesticidas, Fertilizantes
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
    
    return render(request, 'registrarse.html', {
        'form': form
    })

def login_vista(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  
            login(request, user)  
            return redirect('home') 
    else:
        form = AuthenticationForm() 

    return render(request, 'login.html', {
        'form': form
    })

@login_required(login_url='/login/')
def crear_campo(request):
    if request.method == 'POST':
        form = CampoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('admin_campos')
    else:
        form = CampoForm(user=request.user)

    return render(request, 'crear_campo.html', {
        'form': form
    })

@login_required(login_url='/login/')
def admin_campos(request):
    editing = False
    campo_a_editar = None  
    campos = Campo.objects.filter(usuario=request.user)

    # Si es una solicitud POST
    if request.method == 'POST':
        # Eliminar campo
        if 'eliminar_campo_id' in request.POST:
            campo_id = request.POST.get('eliminar_campo_id')
            campo = Campo.objects.get(id=campo_id, usuario=request.user)
            campo.delete()
            return redirect('admin_campos')

        # Si el campo ya existe 
        elif 'campo_id' in request.POST:
            campo_id = request.POST.get('campo_id')
            campo_a_editar = Campo.objects.get(id=campo_id, usuario=request.user)
            form = CampoForm(request.POST, instance=campo_a_editar)
            if form.is_valid():
                form.save()  
                return redirect('admin_campos')
            editing = True  

        # Si es un campo nuevo (sin campo_id)
        else:
            form = CampoForm(request.POST)
            if form.is_valid():
                nuevo_campo = form.save(commit=False)
                nuevo_campo.usuario = request.user
                nuevo_campo.save()
                return redirect('admin_campos')

    # Si es una solicitud GET o estamos en el modo normal de creacion
    else:
        form = CampoForm()

    return render(request, 'admin_campos.html', {
        'campos': campos,
        'form': form,
        'editing': editing,
        'campo_a_editar': campo_a_editar,  # Pasamos el campo que se esta editando
    })

@login_required(login_url='/login/')
def admin_cultivos(request):
    editing = False
    cultivo_a_editar = None  # Variable para almacenar el cultivo que se va a editar

    # Si es una solicitud POST, verificar si es para eliminar o editar
    if request.method == 'POST':
        # Eliminar cultivo
        if 'eliminar_cultivo_id' in request.POST:
            cultivo_id = request.POST.get('eliminar_cultivo_id')
            cultivo = Cultivo.objects.get(id=cultivo_id)
            cultivo.delete()
            return redirect('admin_cultivos')

        # Editar cultivo
        elif 'editar_cultivo_id' in request.POST:
            cultivo_id = request.POST.get('editar_cultivo_id')
            cultivo_a_editar = Cultivo.objects.get(id=cultivo_id)
            form = CultivoForm(instance=cultivo_a_editar, user=request.user)
            editing = True  # Cambiamos el estado a edición

        # Guardar los cambios o crear nuevo cultivo
        else:
            if 'cultivo_id' in request.POST:
                cultivo_a_editar = Cultivo.objects.get(id=request.POST.get('cultivo_id'))
                form = CultivoForm(request.POST, instance=cultivo_a_editar, user=request.user)
                editing = True
            else:
                form = CultivoForm(request.POST, user=request.user)

            if form.is_valid():
                form.save()
                return redirect('admin_cultivos')

    # Si es una solicitud GET o estamos en el modo normal de creación
    if not cultivo_a_editar:
        form = CultivoForm(user=request.user)

    # Obtener los cultivos del usuario actual
    campos_usuario = Campo.objects.filter(usuario=request.user)
    cultivos = Cultivo.objects.filter(campo__in=campos_usuario)

    return render(request, 'admin_cultivos.html', {
        'form': form,
        'cultivos': cultivos,
        'editing': editing,
        'cultivo_a_editar': cultivo_a_editar,
    })

@login_required(login_url='/login/')
def admin_plagas(request):
    editing = False
    plaga_a_editar = None

    # Si es una solicitud POST, verificar si es para eliminar o editar
    if request.method == 'POST':
        # Eliminar plaga
        if 'eliminar_plaga_id' in request.POST:
            plaga_id = request.POST.get('eliminar_plaga_id')
            plaga = Plagas.objects.get(id=plaga_id)
            plaga.delete()
            return redirect('admin_plagas')

        # Editar plaga
        elif 'editar_plaga_id' in request.POST:
            plaga_id = request.POST.get('editar_plaga_id')
            plaga_a_editar = Plagas.objects.get(id=plaga_id)
            form = PlagasForm(instance=plaga_a_editar)
            editing = True  # Cambiamos el estado a edición

        # Guardar los cambios o crear nueva plaga
        else:
            if 'plaga_id' in request.POST:  # Si existe un ID de plaga en el formulario (modo edición)
                plaga_a_editar = Plagas.objects.get(id=request.POST.get('plaga_id'))
                form = PlagasForm(request.POST, instance=plaga_a_editar)
                editing = True
            else:  # Si no, estamos creando una nueva plaga
                form = PlagasForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('admin_plagas')

    # Si es una solicitud GET o estamos en el modo normal de creación
    if not plaga_a_editar:
        form = PlagasForm()

    # Obtener todas las plagas
    plagas = Plagas.objects.all()

    return render(request, 'admin_plagas.html', {
        'form': form,
        'plagas': plagas,
        'editing': editing,
        'plaga_a_editar': plaga_a_editar,
    })


@login_required(login_url='/login/')
def admin_planificaciones(request):
    editing = False
    planificacion_a_editar = None

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

    # Obtener las planificaciones del usuario actual
    planificaciones = PlanificacionCultivo.objects.filter(campo__usuario=request.user)

    return render(request, 'admin_planificaciones.html', {
        'form': form,
        'planificaciones': planificaciones,
        'editing': editing,
        'planificacion_a_editar': planificacion_a_editar,
    })

@login_required(login_url='/login/')
def admin_pesticidas(request):
    editing = False
    pesticida_a_editar = None

    # Si es una solicitud POST, verificar si es para eliminar o editar
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
            form = PesticidaForm(instance=pesticida_a_editar)
            editing = True

        # Guardar cambios o crear nuevo pesticida
        else:
            if 'pesticida_id' in request.POST:
                pesticida_a_editar = Pesticidas.objects.get(id=request.POST.get('pesticida_id'))
                form = PesticidaForm(request.POST, instance=pesticida_a_editar)
                editing = True
            else:
                form = PesticidaForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('admin_pesticidas')

    # Si es una solicitud GET o estamos en el modo normal de creación
    if not pesticida_a_editar:
        form = PesticidaForm()

    # Obtener los pesticidas
    pesticidas = Pesticidas.objects.all()

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
            fertilizante = Fertilizantes.objects.get(id=fertilizante_id)
            fertilizante.delete()
            return redirect('admin_fertilizantes')

        # Editar fertilizante
        elif 'editar_fertilizante_id' in request.POST:
            fertilizante_id = request.POST.get('editar_fertilizante_id')
            fertilizante_a_editar = Fertilizantes.objects.get(id=fertilizante_id)
            form = FertilizanteForm(instance=fertilizante_a_editar)
            editing = True

        # Guardar cambios o crear nuevo fertilizante
        else:
            if 'fertilizante_id' in request.POST:
                fertilizante_a_editar = Fertilizantes.objects.get(id=request.POST.get('fertilizante_id'))
                form = FertilizanteForm(request.POST, instance=fertilizante_a_editar)
                editing = True
            else:
                form = FertilizanteForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('admin_fertilizantes')

    # Si es una solicitud GET o estamos en el modo normal de creación
    if not fertilizante_a_editar:
        form = FertilizanteForm()

    # Obtener los fertilizantes
    fertilizantes = Fertilizantes.objects.all()

    return render(request, 'admin_fertilizantes.html', {
        'form': form,
        'fertilizantes': fertilizantes,
        'editing': editing,
        'fertilizante_a_editar': fertilizante_a_editar,
    })



