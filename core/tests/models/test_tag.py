from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Project, Task, Tag

class TagModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@email.com', password='test_password')
        self.project = Project.objects.create(user=self.user, name='test_Project')
        self.task = Task.objects.create(project=self.project, name='test_task')

        self.tag = Tag.objects.create(name='test_tag')
        self.tag.user_tags.add(self.user)
        self.tag.task_tags.add(self.task)

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'test_tag')
  
    def test_tag_user_many_to_many_relationship(self):
        self.assertIn(self.user, self.tag.user_tags.all())
    
    def test_tag_user_many_to_many_relationship_removal(self):
        self.tag.user_tags.remove(self.user)
        self.assertEqual(self.tag.user_tags.count(), 0)

    def test_tag_task_many_to_many_relationship(self):
        self.assertIn(self.task, self.tag.task_tags.all())

    def test_tag_task_many_to_many_relationship_removal(self):
        self.tag.task_tags.remove(self.task)
        self.assertEqual(self.tag.task_tags.count(), 0)