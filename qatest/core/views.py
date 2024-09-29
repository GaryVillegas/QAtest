from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.db.models import Prefetch
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from .utils.authentication import authenticate_and_redirect
from .utils.plotgenerator import *
from .utils.export_utils import *

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

@login_required
def adminwindow(request):
    casos = Caso.objects.all()
    projects = Project.objects.prefetch_related(Prefetch('responsible_user', queryset=User.objects.all()))
    
    context = {
        'projects': projects,
        'graf': generate_plot_admin(casos) if casos.exists() else '<div><strong>No hay datos disponibles para generar el gráfico.</strong></div>',
        'graf_test': generate_plot_test(casos) if casos.exists() else '<div><strong>No hay datos disponibles para generar el gráfico.</strong></div>',
    }
    return render(request, 'core/admin/admin.html', context)

@login_required
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

@login_required
def users(request):
    
    group_name=['analista', 'dev']
    user_list = User.objects.filter(groups__name__in=group_name)

    context = {
        'user_list': user_list
    }

    return render(request, 'core/admin/users.html', context)

@login_required
def deleteuserpanel(request):
    group_name=['analista', 'dev']
    user_list = User.objects.filter(groups__name__in=group_name)

    context = {
        'user_list': user_list
    }

    return render(request, 'core/admin/deleteuserpanel.html', context)

@login_required
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

@login_required
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
        projects = None

    context = {
        'project_list': projects,
        'message': msg,
        'projectform': project,
    }
    return render(request, 'core/admin/projects.html', context)

@login_required
def deleteprojectpanel(request):
    projects = Project.objects.all()
    context = {
        'project_list': projects
    }

    return render(request, 'core/admin/deleteprojectpanel.html', context)

@login_required
def project(request, project_id):
    try: 
        projects = Project.objects.get(id=project_id)
        caso = Caso.objects.filter(project=project_id)
        users = User.objects.filter(groups__name='analista')

        if request.method == "POST":
            if 'responsible_user' in request.POST:
                user_id = request.POST['responsible_user']
                responsible_user = get_object_or_404(User, id=user_id)
                projects.responsible_user = responsible_user
                projects.save()
                return redirect('project', project_id = project_id)

        context = {
            'project': projects,
            'casos': caso,
            'users': users,
        }
    except Project.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('projects')
    
    return render(request, 'core/admin/projects/project.html', context)

@login_required
def export_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    casos = Caso.objects.filter(project = project)
    data = [{
        'titulo': caso.titulo,
        'estado': caso.estado_display,
        'prioridad': caso.prioridad_display,
        'responsable': caso.user.username
    } for caso in casos]

    if request.GET.get('format') == 'excel':
        return export_to_excel(data, f"{project.name}_casos")
    elif request.GET.get('format') == 'pdf':
        return export_to_pdf(data, f"{project.name}_casos")
    else:
        return HttpResponse("Formato no soportado", status=400)
    
@login_required
def deleteproject(request, pk):
    try:
        project = get_object_or_404(Project, id = pk)
        project.delete()
        return redirect('deleteprojectpanel')
    except Project.DoesNotExist:
        messages.error("Error al buscar la tabla")
        return redirect('deleteprojectpanel')

@login_required
def deleteComment(request, pk):
    try:
        comment = get_object_or_404(Comment, id=pk)
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Comment.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))

@login_required
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
        'graf': gant_plot,
        'projects': projects,
    }

    return render(request, 'core/analista/analista.html', context)

@login_required
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

@login_required
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

@login_required
def caso(request, caso_id):
    caso = get_object_or_404(Caso, id=caso_id)
    comments = Comment.objects.filter(caso=caso)
    commentform = CommentForm()
    if request.method == 'POST':
        if 'commentform' in request.POST:
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
        elif 'prioridad' in request.POST:
            new_prioridad = request.POST['prioridad']
            caso.prioridad = new_prioridad
            caso.save()

    context = {
        'caso': caso,
        'comments': comments,
        'commentform': commentform,
        'estados': Caso.estado_display,
        'prioridad': Caso.prioridad_display,
        'users': users,
    }
    return render(request, 'core/caso.html', context)

@login_required
def dev(request):
    return render(request, 'core/dev/dev.html')