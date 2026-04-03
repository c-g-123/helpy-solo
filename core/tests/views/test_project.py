from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Project


User = get_user_model()


class ProjectViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_create_project_get(self):
        response = self.client.get(reverse('core:create_project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/pages/create-project.html')
        self.assertIn('form', response.context)

    def test_create_project_submit_post_valid(self):
        data = {
            'name': 'Test Project',
        }

        response = self.client.post(reverse('core:create_project_submit'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 1)

        project = Project.objects.first()
        self.assertEqual(project.user, self.user)

    def test_create_project_submit_post_invalid(self):
        response = self.client.post(reverse('core:create_project_submit'), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/pages/create-project.html')
        self.assertContains(response, 'form')

    def test_project_get(self):
        project = Project.objects.create(user=self.user, name='My Project')

        response = self.client.get(reverse('core:project', args=[project.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/pages/project.html')
        self.assertIn('form', response.context)

    def test_project_get_forbidden_for_other_user(self):
        other_user = User.objects.create_user(username='other', password='password123')
        project = Project.objects.create(user=other_user, name='Other Project')

        response = self.client.get(reverse('core:project', args=[project.id]))

        self.assertEqual(response.status_code, 404)

    def test_project_submit_post_valid(self):
        project = Project.objects.create(user=self.user, name='Old Name')

        data = {
            'name': 'Updated Name',
        }

        response = self.client.post(reverse('core:project_submit', args=[project.id]), data)

        self.assertEqual(response.status_code, 302)

        project.refresh_from_db()
        self.assertEqual(project.name, 'Updated Name')

    def test_project_submit_post_invalid(self):
        project = Project.objects.create(user=self.user, name='Old Name')

        response = self.client.post(reverse('core:project_submit', args=[project.id]), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/pages/project.html')

    def test_projects_list(self):
        Project.objects.create(user=self.user, name='Project 1')
        Project.objects.create(user=self.user, name='Project 2')

        response = self.client.get(reverse('core:projects'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/pages/projects.html')
        self.assertEqual(len(response.context['projects']), 2)

    def test_projects_list_only_user_projects(self):
        other_user = User.objects.create_user(username='other', password='password123')

        Project.objects.create(user=other_user, name='Other Project')

        response = self.client.get(reverse('core:projects'))

        self.assertEqual(len(response.context['projects']), 0)
