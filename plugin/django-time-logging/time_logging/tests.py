from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
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


class TimeLogViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_time_log_list_view(self):
        """Test the main time logging page loads correctly."""
        response = self.client.get(reverse('time_logging'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Time Log')
    
    def test_start_time_log(self):
        """Test starting a new time log."""
        response = self.client.post(reverse('start_time_log'), {
            'github_issue_url': 'https://github.com/test/repo/issues/1'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that time log was created
        time_log = TimeLog.objects.filter(user=self.user).first()
        self.assertIsNotNone(time_log)
        self.assertTrue(time_log.is_active)
    
    def test_stop_time_log(self):
        """Test stopping an active time log."""
        # Create an active time log
        time_log = TimeLog.objects.create(
            user=self.user,
            github_issue_url='https://github.com/test/repo/issues/1'
        )
        
        response = self.client.post(reverse('stop_time_log', args=[time_log.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check that time log was stopped
        time_log.refresh_from_db()
        self.assertFalse(time_log.is_active)
        self.assertIsNotNone(time_log.end_time)