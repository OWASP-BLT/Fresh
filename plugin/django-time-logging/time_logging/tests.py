from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import TimeLog

User = get_user_model()


class TimeLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_time_log(self):
        """Test creating a time log entry."""
        time_log = TimeLog.objects.create(
            user=self.user,
            github_issue_url='https://github.com/test/repo/issues/1'
        )
        
        self.assertEqual(time_log.user, self.user)
        self.assertEqual(time_log.github_issue_url, 'https://github.com/test/repo/issues/1')
        self.assertTrue(time_log.is_active)
        self.assertIsNone(time_log.end_time)
    
    def test_stop_time_log(self):
        """Test stopping a time log."""
        time_log = TimeLog.objects.create(
            user=self.user,
            github_issue_url='https://github.com/test/repo/issues/1'
        )
        
        # Stop the time log
        time_log.stop()
        
        self.assertIsNotNone(time_log.end_time)
        self.assertIsNotNone(time_log.duration)
        self.assertFalse(time_log.is_active)
    
    def test_string_representation(self):
        """Test the string representation of TimeLog."""
        time_log = TimeLog.objects.create(
            user=self.user,
            github_issue_url='https://github.com/test/repo/issues/1'
        )
        
        expected = f"TimeLog by {self.user.username} - https://github.com/test/repo/issues/1"
        self.assertEqual(str(time_log), expected)