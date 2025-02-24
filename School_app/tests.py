from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from School_app.models import Teacher, Subject, Student, BusModel
from School_app.serializers import TeacherSerializer, SubjectSerializer, StudentSerializer, BusSerializer


class TeacherTests(APITestCase):

    def setUp(self):
        # Create a sample teacher
        self.teacher_data = {'name': 'John Doe', 'teacher_id': 123}
        self.teacher = Teacher.objects.create(**self.teacher_data)
        self.url = reverse('teacher-list')
        self.invalid_teacher_data = {'name': '', 'teacher_id': ''}

        # Create user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_teacher(self):
        # Test teacher creation with valid data
        response = self.client.post(self.url, self.teacher_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.teacher_data['name'])
        self.assertEqual(response.data['teacher_id'], self.teacher_data['teacher_id'])