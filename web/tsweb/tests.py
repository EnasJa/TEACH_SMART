from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .forms import StudentSignUpForm
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.contrib.auth.hashers import make_password

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from tsweb.views import logout_student 

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

# class StudentSignUpViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.signup_url = reverse('student_signup')

#     def test_signup_GET(self):
#         response = self.client.get(self.signup_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'signup_student.html')

#     def test_signup_POST_valid(self):
#         form_data = {
#             'id_number': '123456789',
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'grade': 'A',
#             'date_of_birth': '2015-01-01',
#             'email': 'john@example.com',
#             'parent_name': 'Jane Doe',
#             'parent_phone': '0501234567',
#             'password': 'testpassword',
#             'confirm_password': 'testpassword'
#         }
#         response = self.client.post(self.signup_url, data=form_data)
#         self.assertRedirects(response, reverse('login_student'))
#         self.assertTrue(Student.objects.filter(email='john@example.com').exists())

#     def test_signup_POST_invalid(self):
#         form_data = {
#             'email': 'invalid_email',
#             'password': 'short',
#             'confirm_password': 'mismatch'
#         }
#         response = self.client.post(self.signup_url, data=form_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'signup_student.html')
#         self.assertContains(response, "Please correct the errors below.")
        
class TeacherViewsTest(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create a teacher and a student for testing
        self.teacher = Teacher.objects.create(id_number="12345", name="Test Teacher", classes="A", subjects="Math")
        self.student = Student.objects.create(name="Test Student", grade="A")

        # Create a user and login
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Set teacher_id in session
        session = self.client.session
        session['teacher_id'] = self.teacher.id_number
        session.save()

    def test_teacher_students_list(self):
        response = self.client.get(reverse('teacher_students_list', args=[self.teacher.id_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_students_list.html')
        self.assertContains(response, self.teacher.name)
        self.assertContains(response, self.student.name)

    def test_profile_teacher(self):
        response = self.client.get(reverse('profile_teacher'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_teacher.html')
        self.assertContains(response, self.teacher.name)

    def test_profile_teacher_no_session(self):
        # Clear the session
        session = self.client.session
        session['teacher_id'] = None
        session.save()

        response = self.client.get(reverse('profile_teacher'))
        self.assertRedirects(response, reverse('login_teacher'))

    def test_profile_teacher_not_found(self):
        # Set an invalid teacher_id in session
        session = self.client.session
        session['teacher_id'] = 'invalid_id'
        session.save()

        response = self.client.get(reverse('profile_teacher'))
        self.assertRedirects(response, reverse('login_teacher'))

class TeacherModelTests(TestCase):
    def setUp(self):
        self.valid_teacher_data = {
            'id_number': '12345',
            'name': 'Test Teacher',
            'classes': 'A',
            'subjects': 'Math'
        }
        self.signup_url = reverse('signup_teacher')

    def test_valid_id_number(self):
        teacher = Teacher(**self.valid_teacher_data)
        try:
            teacher.full_clean()
        except ValidationError as e:
            self.fail(f"Validation error: {e}")

    def test_signup_POST_invalid(self):
        form_data = {
            'id_number': '',
            'name': '',
            'classes': '',
            'subjects': ''
        }
        response = self.client.post(self.signup_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'id_number', 'This field is required.')
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'classes', 'This field is required.')
        self.assertFormError(response, 'form', 'subjects', 'This field is required.')

class StudentModelTests(TestCase):
    def setUp(self):
        self.valid_teacher_data = {
            'id_number': '12345',
            'name': 'Test Teacher',
            'classes': 'A',
            'subjects': 'Math'
        }

    def test_valid_password(self):
        teacher = Teacher(**self.valid_teacher_data)
        teacher.full_clean()

    def test_invalid_id_number(self):
        invalid_teacher_data = self.valid_teacher_data.copy()
        invalid_teacher_data['id_number'] = ''
        teacher = Teacher(**invalid_teacher_data)
        with self.assertRaises(ValidationError):
            teacher.full_clean()




# class LogoutStudentTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='testuser', password='12345')

#     def test_logout_student_post_confirm(self):
#         request = self.factory.post('/logout/', {'confirm_logout': 'true'})
#         request.user = self.user
#         response = logout_student(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('home'))

#     def test_logout_student_post_cancel(self):
#         request = self.factory.post('/logout/')
#         request.user = self.user
#         response = logout_student(request)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('profile_student'))

#     def test_logout_student_get(self):
#         request = self.factory.get('/logout/')
#         request.user = self.user
#         response = logout_student(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'logout.html')
#         self.assertEqual(response.context_data['user_type'], 'student')


class LogoutStudentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_logout_student_post_confirm(self):
        response = self.client.post(reverse('logout_student'), {'confirm_logout': 'true'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_logout_student_post_cancel(self):
        response = self.client.post(reverse('logout_student'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile_student'))

    def test_logout_student_get(self):
        response = self.client.get(reverse('logout_student'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to logout')
        self.assertContains(response, 'student')



class LogoutAdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testadmin', password='12345', is_staff=True)
        self.client.login(username='testadmin', password='12345')

    def test_logout_admin_get(self):
        response = self.client.get(reverse('logout_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')
        self.assertEqual(response.context['user_type'], 'admin')

    def test_logout_admin_post_confirmed(self):
        response = self.client.post(reverse('logout_admin'), {'confirm_logout': 'true'})
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_admin_post_not_confirmed(self):
        response = self.client.post(reverse('logout_admin'), {})
        self.assertRedirects(response, reverse('admin_homepage'))



class LogoutTeacherTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testteacher', password='12345')
        self.client.login(username='testteacher', password='12345')

    def test_logout_teacher_get(self):
        response = self.client.get(reverse('logout_teacher'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')
        self.assertEqual(response.context['user_type'], 'teacher')

    def test_logout_teacher_post_confirmed(self):
        response = self.client.post(reverse('logout_teacher'), {'confirm_logout': 'true'})
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_teacher_post_not_confirmed(self):
        response = self.client.post(reverse('logout_teacher'), {}, follow=True)
        expected_url = reverse('profile_teacher')
        login_url = reverse('login_teacher')
        
        # Check if redirected to profile_teacher or login_teacher
        self.assertTrue(response.redirect_chain[-1][0] in [expected_url, login_url])
        
        if response.redirect_chain[-1][0] == login_url:
            self.assertEqual(response.status_code, 200)
            # Add any additional checks for the login page if needed
        else:
            self.assertEqual(response.status_code, 200)
            # Add any additional checks for the profile page if needed