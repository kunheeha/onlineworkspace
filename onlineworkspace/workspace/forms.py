from django import forms
from tinymce import TinyMCE
from django.forms import ModelForm
from .models import Workspace, Task, Folder, File, Notebook, Note
from django.utils.translation import gettext_lazy as _


class CreateWorkspaceForm(ModelForm):
    class Meta:
        model = Workspace
        fields = ['name', 'desc']
        labels = {
            'desc': _('Short description about workspace')
        }


class TaskQuickAddForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'urgent', 'workspace']
        widgets = {
            'workspace': forms.HiddenInput()
        }


class WorkspaceInviteForm(ModelForm):
    class Meta:
        model = Workspace
        fields = ['users']
        widgets = {
            'users': forms.CheckboxSelectMultiple
        }
        labels = {
            'users': _('Select the usernames of people that should have access to this workspace')
        }


class CreateFolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'workspace']
        widgets = {
            'workspace': forms.HiddenInput()
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'urgent', 'due_date', 'related_folders', 'workspace']
        widgets = {
            'due_date': DateInput(),
            'related_folders': forms.CheckboxSelectMultiple,
            'workspace': forms.HiddenInput()
        }
        labels = {
            'due_date': _('Due Date'),
            'related_folders': _('Select folders related to this task')
        }


class UpdateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'urgent', 'due_date', 'related_folders']
        widgets = {
            'due_date': DateInput(),
            'related_folders': forms.CheckboxSelectMultiple
        }
        labels = {
            'due_date': _('Due Date'),
            'related_folders': _('Select folders related to this task')
        }


class UploadFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'desc', 'filePath', 'folder']
        widgets = {
            'folder': forms.HiddenInput()
        }
        labels = {
            'name': _('Name of File'),
            'desc': _('Short description of File'),
            'filePath': _('File')
        }


class CreateNotebookForm(ModelForm):
    class Meta:
        model = Notebook
        fields = ['title', 'folder']
        widgets = {
            'folder': forms.HiddenInput()
        }


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class CreateNoteForm(ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 10})
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'notebook']
        widgets = {
            'notebook': forms.HiddenInput()
        }


class EditNoteForm(ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 10})
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'notebook']
        widgets = {
            'notebook': forms.HiddenInput()
        }
