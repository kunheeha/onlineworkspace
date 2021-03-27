from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workspace, Folder, Task, File, Notebook, Note
from .forms import CreateWorkspaceForm


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
