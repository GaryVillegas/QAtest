from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='index'),
    path('logout', logout_view, name='logout'),
    path('adminwindow', adminwindow,name='adminwindow'),
    path('adduser', adduser, name='adduser'),
    path('users', users, name='users'),
    path('deleteuserpanel', deleteuserpanel, name='deleteuserpanel'),
    path('deleteuser/<int:user_id>/', deleteuser, name='deleteuser'),
    path('projects', projects, name='projects'),
    path('project/<int:project_id>', project, name='project'),
    path('export_project/<int:project_id>/', export_project, name='export_project'),
    path('deleteprojectpanel', deleteprojectpanel, name='deleteprojectpanel'),
    path('deleteproject/<int:pk>/', deleteproject, name='deleteproject'),
    path('deletecomment/<int:pk>/', deleteComment, name='deletecomment'),
    path('analista', analista, name='analista'),
    path('analista_projects', analista_projects, name='analista_projects'),
    path('analista_project/<int:project_id>', analista_project, name='analista_project'),
    path('caso/<int:caso_id>', caso, name='caso'),
    path('dev', dev, name='dev'),
]