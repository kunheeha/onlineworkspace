from django.urls import path
from .views import (
    DashboardListView, WorkspaceUpdateView, TaskUpdateView, TaskDeleteView,
    FileDeleteView, FolderUpdateView, NotebookUpdateView, NotebookDeleteView,
    FolderDeleteView, NoteUpdateView, NoteDeleteView
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', DashboardListView.as_view(), name='user-dashboard'),
    path('dashboard/new/', views.createWorkspace, name='new-workspace'),
    path('workspace/<int:pk>/edit/',
         WorkspaceUpdateView.as_view(), name='workspace-edit'),
    path('workspace/<int:workspace_id>/',
         views.workspace, name='user-workspace'),
    path('folder/<int:workspace_id>/<int:folder_id>/',
         views.folder, name='user-folder'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),
    path('notebook/<int:workspace_id>/<int:folder_id>/<int:notebook_id>/',
         views.notebook, name='user-notebook'),
    path('folder/<int:pk>/edit/', FolderUpdateView.as_view(), name='folder-edit'),
    path('notebook/<int:pk>/edit/',
         NotebookUpdateView.as_view(), name='notebook-edit'),
    path('notebook/<int:pk>/delete/',
         NotebookDeleteView.as_view(), name='notebook-delete'),
    path('folder/<int:pk>/delete/',
         FolderDeleteView.as_view(), name='folder-delete'),
    path('note/<int:pk>/update/', NoteUpdateView.as_view(), name='note-edit'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete')
]
