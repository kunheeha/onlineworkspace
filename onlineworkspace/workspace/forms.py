from django import forms
from tinymce import TinyMCE
from django.forms import ModelForm
from .models import Workspace, Task, Folder, File, Notebook, Note


class CreateWorkspaceForm(ModelForm):
    class Meta:
        model = Workspace
        fields = ['name', 'desc']


class TaskQuickAddForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'urgent', 'workspace']
        widgets = {
            'workspace': forms.HiddenInput()
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
            'workspace': forms.HiddenInput()
        }


class UpdateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'urgent', 'due_date', 'related_folders']
        widgets = {
            'due_date': DateInput()
        }


class UploadFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'desc', 'filePath', 'folder']
        widgets = {
            'folder': forms.HiddenInput()
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
