from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workspace, Folder, Task, File, Notebook, Note
from .forms import CreateWorkspaceForm, TaskQuickAddForm


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
        if quicktaskform.is_valid():
            quicktaskform.save()
            return redirect('user-workspace', workspace_id=workspace_id)

    quicktaskform = TaskQuickAddForm(initial={'workspace': user_workspace})

    context = {
        'workspace': user_workspace,
        'tasks': tasks,
        'folders': folders,
        'quicktaskform': quicktaskform
    }

    if request.user in user_workspace.users.all():
        return render(request, 'workspace/workspace.html', context)

    return render(request, 'workspace/deniedaccess.html')
