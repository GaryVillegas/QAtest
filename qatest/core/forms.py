from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from .models import *

class Login(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': ''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': ''}))
    
class UserCreator(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ["username", "email", "group"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'password': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form.control', 'placeholder': ''})),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'responsible_user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'responsible_user': forms.Select(attrs={'class': 'form-control'})
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'responsible_user', 'project']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'responsible_user': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widget = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'id': 'comment'})
        }

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ['user', 'project', 'tipo', 'prioridad', 'estimado']
        widget = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'estimado': forms.TextInput(attrs={'class': 'form-control'})   
        }

class CasoContenidoForm(forms.ModelForm):
    class Meta:
        model = CasoContenido
        fields = ['precondicion', 'pasos', 'resultados_esperados']
        widgets = {
            'precondicion': forms.Textarea(attrs={'class': 'form-control'}),
            'pasos': forms.Textarea(attrs={'class': 'form-control'}),
            'resultados_esperados': forms.Textarea(attrs={'class': 'form-control'}),
        }