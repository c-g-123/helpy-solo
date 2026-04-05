from django import forms
from core.models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'parent_project',
            "name",
        ]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Project name",}),}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["parent_project"].queryset = Project.objects.for_user(self.user)  # TODO This NEEDS to check for circular references for the parent project.

    def clean_parent_project(self):
        parent_project = self.cleaned_data["parent_project"]

        if not parent_project:
            return None

        try:
            return Project.objects.for_user(self.user).get(pk=parent_project.pk)
        except Project.DoesNotExist:
            raise forms.ValidationError("Invalid parent project.")
