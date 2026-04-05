from django import forms
from core.models import Project, Task, Resource


INITIAL_DESCRIPTION_ROWS = 3


class TaskForm(forms.ModelForm):

    # TODO This NEEDS to check for circular references for the parent task.

    class Meta:
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["project"].queryset = Project.objects.for_user(self.user)
            self.fields["parent_task"].queryset = Task.objects.for_user(self.user)  # TODO Change this to filter for the project's tasks?

    def clean_project(self):
        project = self.cleaned_data["project"]

        if not Project.objects.for_user(self.user).filter(pk=project.pk).exists():
            raise forms.ValidationError("Invalid project.")

        return project
