from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentSignUpForm
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class StudentModelTest(TestCase):
    def test_student_creation(self):
        student = Student.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            grade='A',
            date_of_birth=date(2015, 1, 1),
            email='john@example.com',
            parent_name='Jane Doe',
            parent_phone='0501234567',
            password='testpassword'
        )
        self.assertEqual(str(student), 'John Doe')
        self.assertTrue(student.password.startswith('pbkdf2_sha256$'))

class StudentSignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('student_signup')

    def test_signup_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_student.html')

    def test_signup_POST_valid(self):
        form_data = {
            'id_number': '123456789',
            'first_name': 'John',
            'last_name': 'Doe',
            'grade': 'A',
            'date_of_birth': '2015-01-01',
            'email': 'john@example.com',
            'parent_name': 'Jane Doe',
            'parent_phone': '0501234567',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        response = self.client.post(self.signup_url, data=form_data)
        self.assertRedirects(response, reverse('login_student'))
        self.assertTrue(Student.objects.filter(email='john@example.com').exists())

    def test_signup_POST_invalid(self):
        form_data = {
            'email': 'invalid_email',
            'password': 'short',
            'confirm_password': 'mismatch'
        }
        response = self.client.post(self.signup_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_student.html')
        self.assertContains(response, "Please correct the errors below.")