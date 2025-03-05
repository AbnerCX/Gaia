from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Campo, Cultivo
from .forms import CampoForm, CultivoForm

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

