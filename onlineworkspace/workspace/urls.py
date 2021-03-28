from django.urls import path
from .views import DashboardListView, WorkspaceUpdateView, TaskUpdateView, TaskDeleteView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', DashboardListView.as_view(), name='user-dashboard'),
    path('dashboard/new/', views.createWorkspace, name='new-workspace'),
    path('workspace/<int:pk>/edit/',
         WorkspaceUpdateView.as_view(), name='workspace-edit'),
    path('workspace/<int:workspace_id>', views.workspace, name='user-workspace'),
    path('folder/<int:workspace_id>/<int:folder_id>/',
         views.folder, name='user-folder'),
    path('task/<int:pk>/edit', TaskUpdateView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete')
]
