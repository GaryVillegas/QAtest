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

def generate_plot_admin(qs):
    casos_data = [{
        'estado': x.estado_display,
        'title': x.project.name
    } for x in qs]
    df = pd.DataFrame(casos_data)
    colors = {
        'Sin Ejecutar': 'grey',
        'Aprobado': 'green',
        'Bloqueado': 'yellow',
        'Retesteado': 'orange',
        'Fallido': 'red', 
    }
    fig = px.pie(df, names='estado', title='Estado de los Casos', color='estado', color_discrete_map=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return plot(fig, output_type='div')

def adminwindow(request):
    qs = Caso.objects.all()
    if qs.exists():
        pie_plot = generate_plot_admin(qs)
        context = {
            'graf': pie_plot
        }
    else:
        context = {
            'graf': '<div>No hay datos disponibles para generar el gráfico.</div>'
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
        caso = Caso.objects.filter(project = project_id)
        casocount = Caso.objects.filter(project = project_id).count()
        context = {
            'project': projects,
            'casos': caso,
            'countcasos': casocount
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
    project = get_object_or_404(Project, id=project_id, responsible_user=actual_user)
    casos = Caso.objects.filter(project=project)

    if request.method == 'POST':
        casoform = CasoForm(request.POST)
        if casoform.is_valid():
            caso = casoform.save(commit=False)
            caso.user = request.user
            caso.project = project
            caso.save()
            return redirect('analista_project', project_id=project_id)
    else:
        casoform = CasoForm(initial={'user': request.user})
        casoform.fields['project'].queryset = Project.objects.filter(responsible_user=actual_user)

    gant_plot = generate_plot_analista(casos)    

    context = {
        'project': project,
        'casos': casos,
        'casoform': casoform,
        'graf': gant_plot
    }
    
    return render(request, 'core/analista/analista_project.html', context)

def generate_plot_analista(casos):
    casos_data = [{
        'estado': caso.estado_display,
        'titulo': caso.project.name
    } for caso in casos]
    df = pd.DataFrame(casos_data)
    if df.empty:
        return '<div>No hay datos disponibles para generar el gráfico.</div>'
    colors = {
        'Sin Ejecutar': 'grey',
        'Aprobado': 'green',
        'Bloqueado': 'yellow',
        'Retesteado': 'orange',
        'Fallido': 'red',
    }
    fig = px.pie(df, names='estado', title='Estado de los Casos', color='estado', color_discrete_map=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return plot(fig, output_type="div")

def caso(request, caso_id):
    caso = get_object_or_404(Caso, id=caso_id)
    comments = Comment.objects.filter(caso=caso)
    if comments == None:
        comments = None
    commentform = CommentForm()
    if request.method == 'POST':
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.user = request.user
            comment.caso = caso
            comment.save()
            return redirect('caso', caso_id=caso_id)
    context = {
        'caso': caso,
        'comments': comments,
        'commentform': commentform
    }
    return render(request, 'core/caso.html', context)

def dev(request):
    return render(request, 'core/dev/dev.html')