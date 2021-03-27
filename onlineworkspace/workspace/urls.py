from django.urls import path
from .views import DashboardListView, WorkspaceUpdateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', DashboardListView.as_view(), name='user-dashboard'),
    path('dashboard/new/', views.createWorkspace, name='new-workspace'),
    path('workspace/<int:pk>/edit/',
         WorkspaceUpdateView.as_view(), name='workspace-edit')
]
