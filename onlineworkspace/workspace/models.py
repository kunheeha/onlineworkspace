from django.db import models
from tinymce import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse


class Workspace(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Workspace {self.name}'

    def get_absolute_url(self):
        return reverse('user-dashboard')


class Folder(models.Model):
    name = models.CharField(max_length=50)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)

    def __str__(self):
        return f'Folder {self.name}, belongs to {self.workspace.name}'


class Task(models.Model):
    name = models.CharField(max_length=50)
    urgent = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    related_folders = models.ManyToManyField(Folder, blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)

    def __str__(self):
        return f'Task {self.name}, belongs to {self.workspace.name}'


def user_directory_path(instance, filename):
    return f'folder_{instance.folder.id}/{filename}'


class File(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100)
    filePath = models.FileField(upload_to=user_directory_path)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return f'File {self.name}, belongs to {self.folder.name} from {self.folder.workspace.name}'

    def delete(self, *args, **kwargs):
        self.filePath.delete()
        super().delete(*args, **kwargs)


class Notebook(models.Model):
    title = models.CharField(max_length=50)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return f'Notebook {self.title}, belongs to {self.folder.name} from {self.folder.workspace.name}'


class Note(models.Model):
    title = models.CharField(max_length=50)
    content = HTMLField()
    last_edited = models.DateTimeField(auto_now=True)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)

    def __str__(self):
        return f'Note {self.title} of {self.notebook.title}'
