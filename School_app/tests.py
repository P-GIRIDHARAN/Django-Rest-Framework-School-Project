from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from School_app.models import Teacher, Subject, Student, BusModel
from School_app.serializers import TeacherSerializer, SubjectSerializer, StudentSerializer, BusSerializer

class TeacherTests(APITestCase):
    def setUp(self):
        self.teacher_data = {
            'name': 'John Doe',
            'teacher_id': 123
        }
        # Correct usage: unpack dictionary with ** to pass keyword arguments
        self.teacher = Teacher.objects.create(**self.teacher_data)
        self.url = reverse('teacher-list')

    def test_create_teacher(self):
            response = self.client.post(self.url, self.teacher_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['name'], self.teacher_data['name'])
            self.assertEqual(response.data['teacher_id'], self.teacher_data['teacher_id'])
