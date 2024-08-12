from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def index(request):
    form = login()
    if request.method == "POST":
        form = login(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                
                if user.username == 'administrador':
                    return redirect('adminwindow')
                
                if request.user.groups.filter(name='analista').exists():
                    return redirect('analista')
                
                if request.user.groups.filter(name='dev').exists():
                    return redirect('dev')
                else:
                    messages.error(request, 'Usuario no esta autorizado para acceder')
                    return redirect('index')
            else:
                messages.error(request, 'Credendiales inválidas. Intentalo de nuevo.')
                return redirect('index')
            
    context = {
        'loginform': form
    }

    return render(request, 'registration/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')

def adminwindow(request):
    return render(request, 'core/admin/admin.html')

def adduser(request):
    
    form = usercreator()
    if request.method == "POST":
        form = usercreator(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                group_id = form.cleaned_data.get("group").id
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                mgs = "ERROR"

            return redirect('users')
            
    context={
        'usercreate': form
    }

    return render(request, 'registration/adduser.html', context)

def users(request):
    
    group_name=['analista', 'dev']
    user_list = User.objects.filter(groups__name__in=group_name)

    context = {
        'user_list': user_list,
    }

    return render(request, 'core/admin/users.html', context)

def deleteuserpanel(request):
    
    group_name=['analista', 'dev']
    user_list = User.objects.filter(groups__name__in=group_name)

    context = {
        'user_list': user_list
    }

    return render(request, 'core/admin/deleteuserpanel.html', context)


def deleteuser(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.user == user:
            return redirect('deleteuserpanel')
        else:
            user.delete()
            return redirect('users')
    except User.DoesNotExist:
        msg = 'error'
        return redirect('users')
    
    return render(request, 'core/admin/deleteuserpanel.html')

def projects(request):
    return render(request, 'core/admin/projects.html')
    

def analista(request):
    return render(request, 'core/analista/analista.html')

def dev(request):
    return render(request, 'core/dev/dev.html')