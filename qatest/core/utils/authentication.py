from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.contrib import messages
from django.shortcuts import redirect

def authenticate_and_redirect(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        
        if user.username == 'administrador':
            return redirect('adminwindow')
        
        if user.groups.filter(name='analista').exists():
            return redirect('analista')
        
        if user.groups.filter(name='dev').exists():
            return redirect('dev')
        else:
            messages.error(request, 'Usuario no esta autorizado para acceder')
            return redirect('index')
    else:
        messages.error(request, 'Credenciales inválidas. Intentalo de nuevo.')
        return redirect('index')