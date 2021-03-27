from django import forms
from django.forms import ModelForm
from .models import Workspace


class CreateWorkspaceForm(ModelForm):
    class Meta:
        model = Workspace
        fields = ['name', 'desc']
