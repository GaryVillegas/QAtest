from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

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

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ['user', 'project', 'titulo', 'tipo', 'prioridad', 'estimado', 'precondicion', 'pasos', 'resultados_esperados']
        widget = {
            'titulo': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'estimado': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'precondicion': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'pasos': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'resultados_esperados': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CasoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                'Detalles del Caso',
                'titulo',
                'tipo',
                'prioridad',
                'estimado',
            ),
            Fieldset(
                'Usuario y Proyecto',
                'user', 'project',
            ),
            Fieldset(
                'Informacion',
                'precondicion',
                'pasos',
                'resultados_esperados'
            )
        )