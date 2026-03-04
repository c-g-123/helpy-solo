from django.contrib import admin
from core.models import Task, Project, Tag, Resource


@admin.register(Project)  # This decorator is the same as writing admin.site.register(Class, ClassAdmin) at the end of this file.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'set_date', 'due_date')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'added_date')
