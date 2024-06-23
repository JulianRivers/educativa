from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout)
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.http import JsonResponse
from .models import (UserProfile)

from .forms import (LoginForm, RegistroForm, UsuarioForm, CambiarPasswordForm)
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from decimal import Decimal
from django.utils import timezone



def loginView(request):
    if request.user.is_superuser:
        return redirect('/admin')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = UserProfile.objects.get(email=email)
            if usuario is not None and usuario.check_password(password):
                login(request, usuario)
                return redirect('producto:inicio') if usuario.is_superuser else redirect('/')
            else:
                messages.error(request, "Contraseña incorrecta")
        except Exception as e:
            messages.error( request, "Lo sentimos, no pudimos encontrar tu cuenta")
            usuario = None
            print(e)
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def index(request):
  
    return render(request, 'index.html')



def logoutView(request):
    logout(request)
    return redirect('/')

def registerView(request):
    if not request.user.is_anonymous: 
        messages.error(request, "Cierre sesión antes de registrar otro usuario.")
        return redirect('/login')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validaciones básicas
        if not all([nombre, apellido, email, password]):
            messages.error(request, "Todos los campos son obligatorios.")
        elif password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
        elif UserProfile.objects.filter(email=email).exists():
            messages.error(request, "El email ya está registrado.")
        else:
            # Crear el nuevo usuario
            user = UserProfile.objects.create_user(
                email=email,
                password=password,
                name=nombre,
                apellidos=apellido
            )
            messages.success(request, "Usuario registrado exitosamente.")
            return redirect('usuario:login')
    
    return render(request, 'registro.html')


def perfil(request):
    usuario = request.user
    form = UsuarioForm(instance=usuario)
    form1 = CambiarPasswordForm()

    context = {
        "form": form,
        "form1": form1,
    }
    
    return render(request, 'perfil.html', context)

def editar_datos(request):
    usuario = request.user
    form1 = CambiarPasswordForm()

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
       
        if form.is_valid():
            password = request.POST.get('password')
            usuario = form.save()
            
            messages.success(request, 'El usuario fue actualizado correctamente')
            return redirect('usuario:login')

    else:
        form = UsuarioForm(instance=usuario)

    context = {
        "form": form,
        "form1": form1
    }
    
    
    # Renderizar el template con los productos
    return render(request, 'perfil.html', context)

def change_password(request):
    usuario = request.user

    form = UsuarioForm(instance=usuario)
    if request.method == 'POST':
        form1 = CambiarPasswordForm(request.POST)
        if form1.is_valid():
            usuario.set_password(form1.cleaned_data['password'])
            usuario.save()
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('usuario:login')
    else:
        form1 = CambiarPasswordForm()

    context = {
        "form": form,
        "form1": form1
    }
    context.update(subcategorias(request))
    
    # Renderizar el template con los productos
    return render(request, 'perfil.html', context)

