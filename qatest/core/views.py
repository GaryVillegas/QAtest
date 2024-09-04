from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import auth, User
from django.contrib import messages
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from django.forms import inlineformset_factory

# Create your views here.
def index(request):
    form = Login()
    if request.method == "POST":
        form = Login(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            form.fields['username'].inital = ''
            form.fields['password'].inital = ''

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
    try:
        qs = Caso.objects.all()
        ticket_data = [
            {
                'User': x.responsible_user.username,
                'Tickets': x.id,
                'Status': x.status
            } for x in qs
        ]

        df = pd.DataFrame(ticket_data)
        fig = px.pie(df, names="Status",  title="Tickets by Projects")

        fig.update_yaxes(autorange="reversed")
        gant_plot = plot(fig, output_type="div")
    except Caso.DoesNotExist:
        gant_plot = None
        messages.error(request, "No se han encontrado tickets.")
    except Exception as e:
        gant_plot = None
        messages.error(request, f"Se produjo un error: {str(e)}")

    context = {
        'graf': gant_plot
    }
    return render(request, 'core/admin/admin.html', context)

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
        'user_list': user_list
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

def deleteprojectpanel(request):

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

def project(request, project_id):
    try: 
        projects = Project.objects.get(id=project_id)
        ticket = Caso.objects.filter(project = project_id)
        ticketcount = Caso.objects.filter(project = project_id).count()
        context = {
            'project': projects,
            'tickets': ticket,
            'counticket': ticketcount
        }
    except Project.DoesNotExist:
        messages.error('error')
    return render(request, 'core/admin/projects/project.html', context)

def deleteproject(request, pk):
    try:
        project = get_object_or_404(Project, id = pk)
        project.delete()
        return redirect('projects')
    except Project.DoesNotExist:
        messages.error("Error al buscar la tabla")
        return redirect('deleteprojectpanel')

def analista(request):
    
    return render(request, 'core/analista/analista.html')

def analista_projects(request):
    actual_user = request.user
    projects = Project.objects.filter(responsible_user = actual_user)

    context = {
        'project': projects
    }

    return render(request, 'core/analista/analista_projects.html', context)

def analista_project(request, project_id):
    actual_user = request.user

    try:
        projects = Project.objects.get(id=project_id, responsible_user = actual_user)
        casos = Caso.objects.filter(project = projects)
        casoform = CasoForm()
        if request.method == 'POST':
            casoform = CasoForm(request.POST)
            if casoform.is_valid():
                caso = casoform.save(commit=False)
                caso.user = request.user
                caso.project = project
                caso.save()
                return redirect('analista_project', project_id=project_id)
        
    except Project.DoesNotExist:
        messages.error(request, 'Error')
        casos = None
        projects = None

    context = {
        'project': projects,
        'casos': casos,
        'casoform': casoform
    }
    
    return render(request, 'core/analista/analista_project.html', context)

def dev(request):
    return render(request, 'core/dev/dev.html')