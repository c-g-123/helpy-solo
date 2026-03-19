from django import forms
from core.models import Project, Task, Resource


class TaskForm(forms.ModelForm):

    class Meta:
        INITIAL_DESCRIPTION_ROWS = 3

        model = Task
        fields = [
            "project",
            "parent_task",
            "name",
            "description",
            "set_datetime",
            "due_datetime",
            'status',
        ]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Task name",}),
            "description": forms.Textarea(attrs={
                "placeholder": "Description",
                "rows": INITIAL_DESCRIPTION_ROWS,
            }),
            "set_datetime": forms.DateTimeInput(attrs={"type": "datetime-local",}),
            "due_datetime": forms.DateTimeInput(attrs={"type": "datetime-local",}),
        }

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get("project")
        parent_task = cleaned_data.get("parent_task")

        if parent_task and parent_task.project != project:
            raise forms.ValidationError("A subtask must belong to the same project as its parent task.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["project"].queryset = Project.objects.filter(user=user)
            self.fields["parent_task"].queryset = Task.objects.filter(project__user=user)
            self.fields["parent_task"].required = False

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'file', 'link']