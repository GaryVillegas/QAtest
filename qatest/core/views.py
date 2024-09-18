from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from .utils.authentication import authenticate_and_redirect
from .utils.plotgenerator import generate_plot_analista, generate_plot_admin

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
            return authenticate_and_redirect(request, username, password)
            
    context = {
        'loginform': form
    }

    return render(request, 'registration/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')

def adminwindow(request):
    casos = Caso.objects.all()
    projects = Project.objects.all()
    
    context = {
        'projects': projects,
        'graf': generate_plot_admin(casos) if casos.exists() else '<div><strong>No hay datos disponibles para generar el gráfico.</strong></div>'
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
    try:
        project = ProjectForm()

        if request.method == "POST":
            project = ProjectForm(request.POST)
            if project.is_valid():
                project.save()
                return redirect('projects')
        msg = ''
    except Project.DoesNotExist:
        msg = 'There are 0 projects at this moment.'

    context = {
        'project_list': projects,
        'message': msg,
        'projectform': project,
    }
    return render(request, 'core/admin/projects.html', context)

def deleteprojectpanel(request):

    projects = Project.objects.all()
    context = {
        'project_list': projects
    }

    return render(request, 'core/admin/deleteprojectpanel.html', context)


def addproject(request):


    return render(request, 'core/admin/addproject.html')

def project(request, project_id):

    try: 
        projects = Project.objects.get(id=project_id)
        caso = Caso.objects.filter(project=project_id)
        casocount = Caso.objects.filter(project=project_id).count()
        users = User.objects.filter(groups__name='analista')

        if request.method == "POST":
            if 'responsible_user' in request.POST:
                user_id = request.POST['responsible_user']
                responsible_user = get_object_or_404(User, id=user_id)
                projects.responsible_user = responsible_user
                projects.save()

        context = {
            'project': projects,
            'casos': caso,
            'countcasos': casocount,
            'users': users,
        }
    except Project.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('projects')
    
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
    projects = Project.objects.filter(responsible_user=request.user)
    casos = Caso.objects.filter(project__in=projects)
    
    try:
        gant_plot = generate_plot_analista(casos)
    except Exception as e:
        gant_plot = None
        messages.error(request, f"Error generating plot: {str(e)}")

    context = {
        'casos': casos,
        'graf': gant_plot
    }

    return render(request, 'core/analista/analista.html', context)

def analista_projects(request):
    try:
        projects = Project.objects.filter(responsible_user = request.user)
    except Project.DoesNotExist:
        messages.error("Error al buscar la tabla")
        projects = None

    context = {
        'project': projects
    }

    return render(request, 'core/analista/analista_projects.html', context)

def analista_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, responsible_user=request.user)
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
        casoform.fields['project'].queryset = Project.objects.filter(responsible_user=request.user)

    gant_plot = generate_plot_analista(casos)    

    context = {
        'project': project,
        'casos': casos,
        'casoform': casoform,
        'graf': gant_plot
    }
    
    return render(request, 'core/analista/analista_project.html', context)

def caso(request, caso_id):
    caso = get_object_or_404(Caso, id=caso_id)
    comments = Comment.objects.filter(caso=caso)
    
    if comments == None:
        comments = None
    commentform = CommentForm()
    if request.method == 'POST':
        if 'comment' in request.POST:
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                comment = commentform.save(commit=False)
                comment.user = request.user
                comment.caso = caso
                comment.save()
                return redirect('caso', caso_id=caso_id)
        elif 'estado' in request.POST:
            new_estado = request.POST['estado']
            caso.estado = new_estado
            caso.save()
            return redirect('caso', caso_id=caso_id)
    
    context = {
        'caso': caso,
        'comments': comments,
        'commentform': commentform,
        'estados': Caso.estado_display
    }
    return render(request, 'core/caso.html', context)

def dev(request):
    return render(request, 'core/dev/dev.html')