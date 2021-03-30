import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workspace, Folder, Task, File, Notebook, Note
from .forms import (
    CreateWorkspaceForm, TaskQuickAddForm, CreateFolderForm,
    CreateTaskForm, UpdateTaskForm, UploadFileForm,
    CreateNotebookForm, CreateNoteForm, EditNoteForm
)


def home(request):
    return render(request, 'workspace/home.html')


class DashboardListView(LoginRequiredMixin, ListView):
    model = Workspace
    template_name = 'workspace/dashboard.html'
    context_object_name = 'workspaces'

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(users=user)


@login_required
def createWorkspace(request):
    if request.method == 'POST':
        form = CreateWorkspaceForm(request.POST)
        if form.is_valid():
            form.save()
            workspace_desc = form.cleaned_data.get('desc')
            new_workspace = Workspace.objects.filter(
                desc=workspace_desc).first()
            new_workspace.users.add(request.user)
            new_workspace.save()
            messages.success(
                request, f'Created new workspace {new_workspace.name}')
            return redirect('user-dashboard')
    else:
        form = CreateWorkspaceForm
    return render(request, 'workspace/new_workspace.html', {'form': form})


class WorkspaceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workspace
    fields = ['name', 'desc']

    def test_func(self):
        workspace = self.get_object()
        if self.request.user in workspace.users.all():
            return True
        return False


@login_required
def workspace(request, *args, **kwargs):
    workspace_id = kwargs['workspace_id']
    user_workspace = Workspace.objects.filter(id=workspace_id).first()
    tasks = Task.objects.filter(workspace=user_workspace)
    folders = Folder.objects.filter(workspace=user_workspace)

    if request.method == 'POST':
        quicktaskform = TaskQuickAddForm(
            request.POST, initial={'workspace': user_workspace})
        createtaskform = CreateTaskForm(
            request.POST, initial={'workspace': user_workspace})
        createfolderform = CreateFolderForm(
            request.POST, initial={'workspace': user_workspace})
        if 'addtask' in request.POST:
            if quicktaskform.is_valid():
                quicktaskform.save()
                return redirect('user-workspace', workspace_id=workspace_id)
        elif 'createtask' in request.POST:
            if createtaskform.is_valid():
                createtaskform.save()
                return redirect('user-workspace', workspace_id=workspace_id)
        elif 'createfolder' in request.POST:
            if createfolderform.is_valid():
                createfolderform.save()
                return redirect('user-workspace', workspace_id=workspace_id)

    quicktaskform = TaskQuickAddForm(initial={'workspace': user_workspace})
    createtaskform = CreateTaskForm(initial={'workspace': user_workspace})
    createfolderform = CreateFolderForm(initial={'workspace': user_workspace})

    context = {
        'workspace': user_workspace,
        'tasks': tasks,
        'folders': folders,
        'quicktaskform': quicktaskform,
        'createtaskform': createtaskform,
        'createfolderform': createfolderform
    }

    if request.user in user_workspace.users.all():
        return render(request, 'workspace/workspace.html', context)

    return render(request, 'workspace/deniedaccess.html')


@login_required
def folder(request, *args, **kwargs):
    workspace_id = kwargs['workspace_id']
    folder_id = kwargs['folder_id']
    user_workspace = Workspace.objects.filter(id=workspace_id).first()
    user_folder = Folder.objects.filter(id=folder_id).first()
    files = File.objects.filter(folder=user_folder)
    notebooks = Notebook.objects.filter(folder=user_folder)

    if request.method == 'POST':
        uploadfileform = UploadFileForm(
            request.POST, request.FILES, initial={'folder': user_folder})
        notebookcreateform = CreateNotebookForm(
            request.POST, initial={'folder': user_folder})
        if 'uploadfile' in request.POST:
            if uploadfileform.is_valid():
                uploadfileform.save()
                return redirect('user-folder', workspace_id=workspace_id, folder_id=folder_id)
        elif 'createnotebook' in request.POST:
            if notebookcreateform.is_valid():
                notebookcreateform.save()
                return redirect('user-folder', workspace_id=workspace_id, folder_id=folder_id)

    uploadfileform = UploadFileForm(initial={'folder': user_folder})
    notebookcreateform = CreateNotebookForm(initial={'folder': user_folder})

    context = {
        'workspace': user_workspace,
        'folder': user_folder,
        'files': files,
        'uploadfileform': uploadfileform,
        'notebooks': notebooks,
        'notebookcreateform': notebookcreateform
    }

    if request.user in user_workspace.users.all():
        return render(request, 'workspace/folder.html', context)

    return render(request, 'workspace/deniedaccess.html')


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm

    def test_func(self):
        task = self.get_object()
        if self.request.user in task.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        task = self.get_object()
        return reverse('user-workspace', kwargs={'workspace_id': task.workspace.id})


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task

    def test_func(self):
        task = self.get_object()
        if self.request.user in task.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        task = self.get_object()
        return reverse('user-workspace', kwargs={'workspace_id': task.workspace.id})


class FileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = File

    def test_func(self):
        file = self.get_object()
        if self.request.user in file.folder.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        folder = self.object.folder
        return reverse('user-folder', kwargs={'workspace_id': folder.workspace.id, 'folder_id': folder.id})


@login_required
def notebook(request, *args, **kwargs):
    workspace_id = kwargs['workspace_id']
    folder_id = kwargs['folder_id']
    notebook_id = kwargs['notebook_id']
    user_workspace = Workspace.objects.filter(id=workspace_id).first()
    user_folder = Folder.objects.filter(id=folder_id).first()
    user_notebook = Notebook.objects.filter(id=notebook_id).first()
    notes = Note.objects.filter(notebook=user_notebook)

    if request.method == 'POST':
        createnoteform = CreateNoteForm(
            request.POST, initial={'notebook': user_notebook})
        if 'createnote' in request.POST:
            if createnoteform.is_valid():
                createnoteform.save()
                return redirect('user-notebook', workspace_id=workspace_id, folder_id=folder_id, notebook_id=notebook_id)

    createnoteform = CreateNoteForm(initial={'notebook': user_notebook})

    context = {
        'workspace': user_workspace,
        'folder': user_folder,
        'notebook': user_notebook,
        'notes': notes,
        'createnoteform': createnoteform,
    }

    if request.user in user_workspace.users.all():
        return render(request, 'workspace/notebook.html', context)

    return render(request, 'workspace/deniedaccess.html')


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = EditNoteForm

    def test_func(self):
        note = self.get_object()
        if self.request.user in note.notebook.folder.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        notebook = self.object.notebook
        return reverse('user-notebook', kwargs={'workspace_id': notebook.folder.workspace.id, 'folder_id': notebook.folder.id, 'notebook_id': notebook.id})


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note

    def test_func(self):
        note = self.get_object()
        if self.request.user in note.notebook.folder.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        notebook = self.object.notebook
        return reverse('user-notebook', kwargs={'workspace_id': notebook.folder.workspace.id, 'folder_id': notebook.folder.id, 'notebook_id': notebook.id})


class FolderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Folder
    fields = ['name']

    def test_func(self):
        folder = self.get_object()
        if self.request.user in folder.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        folder = self.get_object()
        return reverse('user-folder', kwargs={'workspace_id': folder.workspace.id, 'folder_id': folder.id})


class NotebookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Notebook
    fields = ['title']

    def test_func(self):
        notebook = self.get_object()
        if self.request.user in notebook.folder.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        notebook = self.get_object()
        return reverse('user-notebook', kwargs={'workspace_id': notebook.folder.workspace.id, 'folder_id': notebook.folder.id, 'notebook_id': notebook.id})


class NotebookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Notebook

    def test_func(self):
        notebook = self.get_object()
        if self.request.user in notebook.folder.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        folder = self.object.folder
        return reverse('user-folder', kwargs={'workspace_id': folder.workspace.id, 'folder_id': folder.id})


class FolderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Folder

    def test_func(self):
        folder = self.get_object()
        if self.request.user in folder.workspace.users.all():
            return True
        return False

    def get_success_url(self):
        folder = self.get_object()
        return reverse('user-workspace', kwargs={'workspace_id': folder.workspace.id})
