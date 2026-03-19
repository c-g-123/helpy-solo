from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Project, Task
from django.core.exceptions import ValidationError

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@email.com', password='test_password')
        self.project = Project.objects.create(user=self.user, name='test_Project')
        
        self.parent_task = Task.objects.create(
            project=self.project,
            name='Parent_task',
            description='This is the top-level task',
            status=Task.Status.TODO
        )

        self.child_task = Task.objects.create(
            project=self.project,
            name='Child_task',
            parent_task=self.parent_task,
            status=Task.Status.IN_PROGRESS
        )

    def test_task_name(self):
        self.assertEqual(self.parent_task.name, 'Parent_task')

    def test_task_status(self):
        self.assertEqual(self.parent_task.status, 'TODO')
    
    def test_task_name_is_str(self):
        self.assertEqual(str(self.parent_task), 'Parent_task')

    def test_task_parent_task_has_no_parent(self):
        self.assertIsNone(self.parent_task.parent_task)

    def test_task_name_max_length(self):
        test_name = 'a' * (Task.MAX_NAME_LENGTH + 1)
        task = Task(name=test_name)

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_description_max_length(self):
        test_description = 'a' * (Task.MAX_DESCRIPTION_LENGTH + 1)
        task = Task(description=test_description)

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_status_max_length(self):                    #Why do we need MAX_STATUS_LENGTH if we have options to chooe from?
        test_status = 'a' * (Task.MAX_STATUS_LENGTH + 1)
        task = Task(status=test_status)

        with self.assertRaises(ValidationError):
            task.full_clean()