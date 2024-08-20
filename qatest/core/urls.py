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
    path('addproject', addproject, name='addproject'),
    path('project', project, name='project'),
    path('deleteprojectpanel', deleteprojectpanel, name='deleteprojectpanel'),
    path('deleteproject/<str:pk>/', deleteproject, name='deleteproject'),
    path('analista', analista, name='analista'),
    path('analista_projects', analista_projects, name='analista_projects'),
    path('dev', dev, name='dev'),
]