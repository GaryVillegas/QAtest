from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def index(request):
    form = Login()
    if request.method == "POST":
        form = Login(request, data=request.POST)
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
    
    form = UserCreator()
    if request.method == "POST":
        form = UserCreator(request.POST)
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

    projects = Project.objects.all()
    msg = ''
    if not projects:
        msg = 'There are 0 projects at this moment.'
    context = {
        'project_list': projects,
        'message': msg
    }
    return render(request, 'core/admin/projects.html', context)

def deleleprojectpanel(request):

    projects = Project.objects.all()
    context = {
        'project_list': projects
    }

    return render(request, 'core/admin/deleteprojectpanel.html', context)

def addproject(request):
    project = ProjectForm()

    if request.method == "POST":
        project = ProjectForm(request.POST)
        if project.is_valid():
            project.save()
            return redirect('projects')

    context = {
        'projectform': project
    }

    return render(request, 'core/admin/addproject.html', context)

def project(request):
    return render(request, 'core/admin/projects/project.html')

def analista(request):
    return render(request, 'core/analista/analista.html')

def analista_projects(request):
    return render(request, 'core/analista/analista_projects.html')

def dev(request):
    return render(request, 'core/dev/dev.html')