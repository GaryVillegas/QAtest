from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='index'),
    path('logout', logout_view, name='logout'),
    path('adminwindow', adminwindow,name='adminwindow'),
    path('adduser', adduser, name='adduser'),
    path('analista', analista, name='analista'),
    path('dev', dev, name='dev')
]