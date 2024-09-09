from django.test import TestCase
from .models import User, Course  # import your models here

class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(user.username, 'testuser')

class CourseModelTests(TestCase):
    def test_course_creation(self):
        # Create a teacher user first
        teacher = User.objects.create_user(username='testteacher', password='testpass', user_type='teacher')

        # Now create a course and assign the teacher
        course = Course.objects.create(title='Test Course', description='Test Description', teacher=teacher)
        
        # Verify the course is created with the correct title and teacher
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.teacher, teacher)
