from django import forms
from core.models import Project, Task


INITIAL_DESCRIPTION_ROWS = 3


class TaskForm(forms.ModelForm):

    # TODO This NEEDS to check for circular references for the parent task.

    class Meta:
        model = Task
        fields = [
            'user',
            "project",
            "parent_task",
            'recurrence_source',
            "name",
            "description",
            "due_datetime",
            'status',
        ]

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Task name",}),
            "description": forms.Textarea(attrs={
                "placeholder": "Description",
                "rows": INITIAL_DESCRIPTION_ROWS,
            }),
            "due_datetime": forms.DateTimeInput(attrs={"type": "datetime-local",}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["user"].disabled = True
            self.fields['user'].initial = self.user
            self.fields["project"].queryset = Project.objects.filter(user=self.user)
            self.fields["parent_task"].queryset = Task.objects.filter(user=self.user)  # TODO Filter this to be tasks from the same project only?
            self.fields['recurrence_source'].disabled = True

    def save(self, commit=True):
        task = super().save(commit=False)
        task.user = self.user

        if commit:
            task.save()

        return task
