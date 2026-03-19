from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Project, Task

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
