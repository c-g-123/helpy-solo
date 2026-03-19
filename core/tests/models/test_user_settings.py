from django.test import TestCase
from django.contrib.auth.models import User
from core.models import UserSettings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class UserSettingsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@email.com', password='test_password')
        self.user_settings = UserSettings.objects.create(
            user=self.user,
            theme=UserSettings.Theme.DARK,
            default_board=UserSettings.DefaultBoard.KANBAN
        )

    def test_user_settings_theme(self):
        self.assertEqual(self.user_settings.theme, 'DARK')

    def test_user_settings_defaut_board(self):
        self.assertEqual(self.user_settings.default_board, 'KANBAN')

    def test_user_settings_name_is_str(self):
        self.assertEqual(str(self.user_settings), "test_user's settings")

    def test_user_settings_theme_that_is_not_an_option(self):
        self.user_settings.theme = 'NEON'
        with self.assertRaises(ValidationError):
            self.user_settings.full_clean()

    def test_user_settings_only_one_settings_profile_per_user(self):
        with self.assertRaises(IntegrityError):
            UserSettings.objects.create(user=self.user, theme=UserSettings.Theme.DARK)
