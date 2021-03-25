from django.contrib import admin
from .models import Workspace, Folder, Task, File, Notebook, Note

# Register your models here.
admin.site.register(Workspace)
admin.site.register(Folder)
admin.site.register(Task)
admin.site.register(File)
admin.site.register(Notebook)
admin.site.register(Note)
