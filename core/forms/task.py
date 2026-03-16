from django import forms
from core.models import Project, Task


class TaskForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('TODO', 'ToDo'),
        ('IP', 'In Progress'),
        ('DONE', 'Done')
    ]
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Name"
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Description"
        })
    )

    set_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    due_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            "project",
            "parent_task",
            "name",
            "description",
            "set_datetime",
            "due_datetime",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["project"].queryset = Project.objects.filter(user=user)
            self.fields["parent_task"].queryset = Task.objects.filter(project__user=user)
            self.fields["parent_task"].required = False

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get("project")
        parent_task = cleaned_data.get("parent_task")

        if parent_task and parent_task.project != project:
            raise forms.ValidationError("A subtask must belong to the same project as its parent task.")

        return cleaned_data
