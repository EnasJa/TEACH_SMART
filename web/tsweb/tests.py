import unittest
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .forms import StudentSignUpForm
from django.core.exceptions import ValidationError
from datetime import date, timedelta, timezone
from django.contrib.auth.hashers import make_password
from datetime import date
from .forms import *
from django.contrib.auth.hashers import check_password
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from tsweb.views import logout_student 
from django.contrib import messages
from django.contrib.messages import get_messages

# class StudentModelTest(TestCase):
#     def test_student_creation(self):
#         # Create the student without setting the password directly
#         student = Student.objects.create(
#             id_number='123456789',
#             first_name='John',
#             last_name='Doe',
#             grade='A',
#             date_of_birth=date(2015, 1, 1),
#             email='john@example.com',
#             parent_name='Jane Doe',
#             parent_phone='0501234567'
#         )
        
#         # Set and hash the password
#         student.set_password('testpassword')
#         student.save()
#             parent_phone='0501234567',
#             password='testpassword'
#         )
#         self.assertEqual(str(student), 'John Doe')
#         self.assertTrue(student.password.startswith('pbkdf2_sha256$'))

#         # Check if the __str__ method returns the correct full name
#         self.assertEqual(str(student), 'John Doe')
        
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
        
# class TeacherViewsTest(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Create a teacher and a student for testing
#         self.teacher = Teacher.objects.create(id_number="12345", name="Test Teacher", classes="A", subjects="Math")
#         self.student = Student.objects.create(name="Test Student", grade="A")

#         # Create a user and login
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.client.login(username='testuser', password='12345')

#         # Set teacher_id in session
#         session = self.client.session
#         session['teacher_id'] = self.teacher.id_number
#         session.save()

#     def test_teacher_students_list(self):
#         response = self.client.get(reverse('teacher_students_list', args=[self.teacher.id_number]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'teacher_students_list.html')
#         self.assertContains(response, self.teacher.name)
#         self.assertContains(response, self.student.name)

#     def test_profile_teacher(self):
#         response = self.client.get(reverse('profile_teacher'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'profile_teacher.html')
#         self.assertContains(response, self.teacher.name)

#     def test_profile_teacher_no_session(self):
#         # Clear the session
#         session = self.client.session
#         session['teacher_id'] = None
#         session.save()

#         response = self.client.get(reverse('profile_teacher'))
#         self.assertRedirects(response, reverse('login_teacher'))

#     def test_profile_teacher_not_found(self):
#         # Set an invalid teacher_id in session
#         session = self.client.session
#         session['teacher_id'] = 'invalid_id'
#         session.save()

#         response = self.client.get(reverse('profile_teacher'))
#         self.assertRedirects(response, reverse('login_teacher'))

# class TeacherModelTests(TestCase):
#     def setUp(self):
#         self.valid_teacher_data = {
#             'id_number': '12345',
#             'name': 'Test Teacher',
#             'classes': 'A',
#             'subjects': 'Math'
#         }
#         self.signup_url = reverse('signup_teacher')

#     def test_valid_id_number(self):
#         teacher = Teacher(**self.valid_teacher_data)
#         try:
#             teacher.full_clean()
#         except ValidationError as e:
#             self.fail(f"Validation error: {e}")

#     def test_signup_POST_invalid(self):
#         form_data = {
#             'id_number': '',
#             'name': '',
#             'classes': '',
#             'subjects': ''
#         }
#         response = self.client.post(self.signup_url, data=form_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(response, 'form', 'id_number', 'This field is required.')
#         self.assertFormError(response, 'form', 'name', 'This field is required.')
#         self.assertFormError(response, 'form', 'classes', 'This field is required.')
#         self.assertFormError(response, 'form', 'subjects', 'This field is required.')

# class StudentModelTests(TestCase):
#     def setUp(self):
#         self.valid_teacher_data = {
#             'id_number': '12345',
#             'name': 'Test Teacher',
#             'classes': 'A',
#             'subjects': 'Math'
#         }

#     def test_valid_password(self):
#         teacher = Teacher(**self.valid_teacher_data)
#         teacher.full_clean()

#     def test_invalid_id_number(self):
#         invalid_teacher_data = self.valid_teacher_data.copy()
#         invalid_teacher_data['id_number'] = ''
#         teacher = Teacher(**invalid_teacher_data)
#         with self.assertRaises(ValidationError):
#             teacher.full_clean()

# class TeacherModelTests(TestCase):
#     def setUp(self):
#         self.valid_teacher_data = {
#             'id_number': '12345',
#             'name': 'Test Teacher',
#             'classes': 'A',
#             'subjects': 'Math'
#         }
#         self.signup_url = reverse('signup_teacher')

#     def test_valid_id_number(self):
#         teacher = Teacher(**self.valid_teacher_data)
#         try:
#             teacher.full_clean()
#         except ValidationError as e:
#             self.fail(f"Validation error: {e}")

#     def test_signup_POST_invalid(self):
#         form_data = {
#             'id_number': '',
#             'name': '',
#             'classes': '',
#             'subjects': ''
#         }
#         response = self.client.post(self.signup_url, data=form_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(response, 'form', 'id_number', 'This field is required.')
#         self.assertFormError(response, 'form', 'name', 'This field is required.')
#         self.assertFormError(response, 'form', 'classes', 'This field is required.')
#         self.assertFormError(response, 'form', 'subjects', 'This field is required.')

# class StudentModelTests(TestCase):
#     def setUp(self):
#         self.valid_teacher_data = {
#             'id_number': '12345',
#             'name': 'Test Teacher',
#             'classes': 'A',
#             'subjects': 'Math'
#         }

#     def test_valid_password(self):
#         teacher = Teacher(**self.valid_teacher_data)
#         teacher.full_clean()

#     def test_invalid_id_number(self):
#         invalid_teacher_data = self.valid_teacher_data.copy()
#         invalid_teacher_data['id_number'] = ''
#         teacher = Teacher(**invalid_teacher_data)
#         with s  
# #===================================================================
        
        
# # class LogoutStudentTestCase(TestCase):
# #     def setUp(self):
# #         self.factory = RequestFactory()
# #         self.user = User.objects.create_user(username='testuser', password='12345')

# #     def test_logout_student_post_confirm(self):
# #         request = self.factory.post('/logout/', {'confirm_logout': 'true'})
# #         request.user = self.user
# #         response = logout_student(request)
# #         self.assertEqual(response.status_code, 302)
# #         self.assertEqual(response.url, reverse('home'))

# #     def test_logout_student_post_cancel(self):
# #         request = self.factory.post('/logout/')
# #         request.user = self.user
# #         response = logout_student(request)
# #         self.assertEqual(response.status_code, 302)
# #         self.assertEqual(response.url, reverse('profile_student'))

# #     def test_logout_student_get(self):
# #         request = self.factory.get('/logout/')
# #         request.user = self.user
# #         response = logout_student(request)
# #         self.assertEqual(response.status_code, 200)
# #         self.assertTemplateUsed(response, 'logout.html')
# #         self.assertEqual(response.context_data['user_type'], 'student')


# class LogoutStudentTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.client.login(username='testuser', password='12345')

#     def test_logout_student_post_confirm(self):
#         response = self.client.post(reverse('logout_student'), {'confirm_logout': 'true'})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('home'))

#     def test_logout_student_post_cancel(self):
#         response = self.client.post(reverse('logout_student'))
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse('profile_student'))

#     def test_logout_student_get(self):
#         response = self.client.get(reverse('logout_student'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Are you sure you want to logout')
#         self.assertContains(response, 'student')



# class LogoutAdminTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testadmin', password='12345', is_staff=True)
#         self.client.login(username='testadmin', password='12345')

#     def test_logout_admin_get(self):
#         response = self.client.get(reverse('logout_admin'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'logout.html')
#         self.assertEqual(response.context['user_type'], 'admin')

#     def test_logout_admin_post_confirmed(self):
#         response = self.client.post(reverse('logout_admin'), {'confirm_logout': 'true'})
#         self.assertRedirects(response, reverse('home'))
#         self.assertFalse('_auth_user_id' in self.client.session)

#     def test_logout_admin_post_not_confirmed(self):
#         response = self.client.post(reverse('logout_admin'), {})
#         self.assertRedirects(response, reverse('admin_homepage'))



# class LogoutTeacherTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testteacher', password='12345')
#         self.client.login(username='testteacher', password='12345')

#     def test_logout_teacher_get(self):
#         response = self.client.get(reverse('logout_teacher'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'logout.html')
#         self.assertEqual(response.context['user_type'], 'teacher')

#     def test_logout_teacher_post_confirmed(self):
#         response = self.client.post(reverse('logout_teacher'), {'confirm_logout': 'true'})
#         self.assertRedirects(response, reverse('home'))
#         self.assertFalse('_auth_user_id' in self.client.session)

#     def test_logout_teacher_post_not_confirmed(self):
#         response = self.client.post(reverse('logout_teacher'), {}, follow=True)
#         expected_url = reverse('profile_teacher')
#         login_url = reverse('login_teacher')
        
#         # Check if redirected to profile_teacher or login_teacher
#         self.assertTrue(response.redirect_chain[-1][0] in [expected_url, login_url])
        
#         if response.redirect_chain[-1][0] == login_url:
#             self.assertEqual(response.status_code, 200)
#             # Add any additional checks for the login page if needed
#         else:
#             self.assertEqual(response.status_code, 200)
#             # Add any additional checks for the profile page if needed
#--------------------------new tests--------------------------------------
#============================uint test for login student================================
class StudentLoginFormTest(TestCase):

    def test_form_valid_data(self):
        form = StudentLoginForm(data={
            'id_number': '123456789',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_id_number(self):
        form = StudentLoginForm(data={
            'id_number': '12345',  # Invalid ID (less than 9 digits)
            'password': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('id_number', form.errors)
        
    
class StudentLoginViewTest(TestCase):

    def setUp(self):
        # Ensure password is hashed when creating the student
        self.student = Student.objects.create(
            id_number='123456789',
            first_name='Test',
            last_name='Student',
            grade='A',
            date_of_birth='2008-05-15',
            email='teststudent@example.com',
            parent_name='Parent Name',
            parent_phone='0501234567',
            password=make_password('password123')  # Ensure password is hashed
        )

    def test_login_view_post_success(self):
        # Simulate a POST request to login with correct credentials
        response = self.client.post(reverse('login_student'), {
            'id_number': '123456789',
            'password': 'password123'  # Use the correct password
        })

        # Check if the response redirects to the profile page (status code 302)
        self.assertRedirects(response, reverse('profile_student'))

        # Check if the session is correctly set
        self.assertEqual(self.client.session['student_id'], '123456789')

    def test_login_view_get(self):
        # Test the GET request for the login page
        response = self.client.get(reverse('login_student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_student.html')

    def test_login_view_post_invalid_id(self):
        # Test with an incorrect ID
        response = self.client.post(reverse('login_student'), {
            'id_number': '987654321',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid ID number')

    def test_login_view_post_invalid_password(self):
        # Test with an incorrect password
        response = self.client.post(reverse('login_student'), {
            'id_number': '123456789',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid password')
#============================ unit test login teacher=======================
class TeacherModelTest(TestCase):
    def setUp(self):
        # Create a subject for the ForeignKey relationship
        self.subject = Subject.objects.create(name="Math")

    def test_create_teacher(self):
        # Create a teacher instance
        teacher = Teacher.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            date_of_birth='1980-01-01',
            email='john.doe@example.com',
            phone_number='0501234567',
            password='password123',
            subject=self.subject,
            classes='A'
        )


        # Test if the teacher was created successfully
        self.assertEqual(teacher.first_name, 'John')
        self.assertEqual(teacher.last_name, 'Doe')
        self.assertEqual(teacher.email, 'john.doe@example.com')
        self.assertTrue(check_password('password123', teacher.password))

    def test_invalid_phone_number(self):
        teacher = Teacher(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            date_of_birth='1980-01-01',
            email='john.doe@example.com',
            phone_number='1234567890',  # Invalid phone number
            password='password123',
            subject=self.subject,
            classes='A'
        )
        with self.assertRaises(ValidationError):
            teacher.full_clean()  # This will validate the model

    def test_invalid_id_number(self):
        teacher = Teacher(
            id_number='123',  # Invalid ID number
            first_name='John',
            last_name='Doe',
            date_of_birth='1980-01-01',
            email='john.doe@example.com',
            phone_number='0501234567',
            password='password123',
            subject=self.subject,
            classes='A'
        )
        with self.assertRaises(ValidationError):
            teacher.full_clean()  # This will validate the model

    def test_invalid_email(self):
        teacher = Teacher(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            date_of_birth='1980-01-01',
            email='invalid-email',  # Invalid email
            phone_number='0501234567',
            password='password123',
            subject=self.subject,
            classes='A'
        )
        with self.assertRaises(ValidationError):
            teacher.full_clean()  # This will validate the model

class LoginTeacherFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'id_number': '123456789',
            'password': 'password123'
        }
        form = loginTeacherForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_id_number(self):
        form_data = {
            'id_number': '123',  # Invalid ID number
            'password': 'password123'
        }
        form = loginTeacherForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ID number must be exactly 9 digits.', form.errors['id_number'])

    def test_missing_password(self):
        form_data = {
            'id_number': '123456789',
            'password': ''  # Missing password
        }
        form = loginTeacherForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['password'])        
   
#=============================================================================================

#================unit test profie student=================================
class StudentModelTest(TestCase):
    def setUp(self):
        # Set up a student instance for the tests
        self.student = Student.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            grade='A',
            date_of_birth='2010-01-01',
            email='john.doe@example.com',
            parent_name='Jane Doe',
            parent_phone='0501234567'
        )

    def test_student_creation(self):
        # Test that the student instance is created correctly
        self.assertEqual(self.student.first_name, 'John')
        self.assertEqual(self.student.grade, 'A')
        self.assertEqual(self.student.email, 'john.doe@example.com')

    def test_invalid_phone_number(self):
        # Test invalid phone number
        student = Student(
            id_number='987654321',
            first_name='Jane',
            last_name='Smith',
            grade='B',
            date_of_birth='2011-01-01',
            email='jane.smith@example.com',
            parent_name='John Smith',
            parent_phone='1234567890'  # Invalid phone number
        )
        with self.assertRaises(ValidationError):
            student.full_clean()  # This will validate the model

    def test_invalid_id_number(self):
        # Test invalid ID number
        student = Student(
            id_number='123',  # Invalid ID number
            first_name='Jane',
            last_name='Smith',
            grade='B',
            date_of_birth='2011-01-01',
            email='jane.smith@example.com',
            parent_name='John Smith',
            parent_phone='0501234567'
        )
        with self.assertRaises(ValidationError):
            student.full_clean()  # This will validate the model

class ProfileStudentViewTest(TestCase):
    def setUp(self):
        # Create a student instance for the test
        self.student = Student.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            grade='A',
            date_of_birth='2010-01-01',
            email='john.doe@example.com',
            parent_name='Jane Doe',
            parent_phone='0501234567'
        )

    def test_profile_student_with_valid_student_id(self):
        # Simulate a session with a valid student ID
        session = self.client.session
        session['student_id'] = '123456789'
        session.save()

        # Make a GET request to the profile_student view
        response = self.client.get(reverse('profile_student'))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

    def test_profile_student_with_invalid_student_id(self):
        # Simulate a session with an invalid student ID
        session = self.client.session
        session['student_id'] = '987654321'  # Non-existent student ID
        session.save()

        # Make a GET request to the profile_student view
        response = self.client.get(reverse('profile_student'))

        # Check that the user is redirected to the login page
        self.assertRedirects(response, reverse('login_student'))

        # Check that an error message is shown
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Student not found')

    def test_profile_student_without_student_id_in_session(self):
        # Make a GET request to the profile_student view without a session
        response = self.client.get(reverse('profile_student'))

        # Check that the user is redirected to the login page
        self.assertRedirects(response, reverse('login_student'))
#======================================================

#=================== unit test about us==========================
class AboutUsViewTest(TestCase):
    def test_about_us_view(self):
        # Make a GET request to the 'about_us' view
        response = self.client.get(reverse('about_us'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'about_us.html')

        # Check if the page contains the expected title and content
        self.assertContains(response, '<h1>About Us</h1>')
        self.assertContains(response, '<h2>The Problem</h2>')
        self.assertContains(response, '<h2>Our Solution</h2>')
        self.assertContains(response, '<h2>Our Team</h2>')
        self.assertContains(response, '<h2>Our Vision</h2>')
 #====================================================================================================  
 
from django.contrib.messages import get_messages

class CreateExamViewTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='Math')
        self.teacher = Teacher.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            date_of_birth='1980-01-01',
            email='john.doe@example.com',
            phone_number='0501234567',
            subject=self.subject
        )
        self.subject_class = SubjectClass.objects.create(class_name='A', subject=self.subject)
        self.subject_class.teachers.add(self.teacher)
    
    def test_create_exam_get_request_without_logged_in_teacher(self):
        response = self.client.get(reverse('create_exam'))
        self.assertRedirects(response, reverse('login_teacher'))
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'You must be logged in to create an exam.')

    def test_create_exam_post_request_valid_data(self):
        session = self.client.session
        session['teacher_id'] = '123456789'
        session.save()
        
        form_data = {
            'subject': self.subject.pk,
            'difficulty': 'easy',
            'material': 'Algebra',
            'num_questions': 10,
            'max_grade': 100,
            'grade': 'A'
        }
        response = self.client.post(reverse('create_exam'), data=form_data)
        
        self.assertEqual(Exam.objects.count(), 1)
        exam = Exam.objects.first()
        self.assertEqual(exam.teacher_id, self.teacher.id_number)  # Ensure this matches the type used in the model
        self.assertRedirects(response, reverse('review_exam', args=[exam.pk]))

#==================================== unit test for review exam ==============================================
class ExamTestCase(TestCase):

    def setUp(self):
        # Set up the necessary objects for the tests
        self.subject = Subject.objects.create(name="Mathematics")
        self.teacher = Teacher.objects.create(
            id_number="123456789",
            first_name="John",
            last_name="Doe",
            date_of_birth="1980-01-01",
            email="johndoe@example.com",
            phone_number="0501234567",
            password="password123",
            subject=self.subject,
            classes='A'
        )
        self.exam = Exam.objects.create(
            subject=self.subject,
            difficulty="medium",
            material="Mathematics material",
            num_questions=5,
            max_grade=100,
            grade="A",
            is_approved=False,
            teacher_id=self.teacher.id_number
        )
        self.question1 = Question.objects.create(
            exam=self.exam,
            text="What is 2+2?",
            choices={"A": "3", "B": "4", "C": "5"},
            correct_answer="B",
            is_approved=False
        )
        self.question2 = Question.objects.create(
            exam=self.exam,
            text="What is 3+3?",
            choices={"A": "6", "B": "7", "C": "8"},
            correct_answer="A",
            is_approved=False
        )

    def test_review_exam_view(self):
        # Approve the question
        self.question1.is_approved = True
        self.question1.save()
        
        # Check if the question is approved
        self.assertTrue(self.question1.is_approved)
        
        # Check the review_exam view
        response = self.client.get(reverse('review_exam', args=[self.exam.pk]))
        self.assertEqual(response.status_code, 200)


    def test_partial_approval(self):
        # Log in the test client
        self.client.login(username='testuser', password='testpassword')

        # Post the request and follow redirects
        response = self.client.post(reverse('review_exam', args=[self.exam.pk]), {'approved_questions': [self.exam.question_set.first().id]}, follow=True)

        # Check if the redirection is correct
        self.assertRedirects(response, reverse('login_teacher'))

    def test_teacher_str(self):
        # Test the string representation of the Teacher model
        self.assertEqual(str(self.teacher), "John Doe")

    def test_exam_str(self):
        # Test the string representation of the Exam model
        self.assertEqual(str(self.exam), "Mathematics - A by Teacher ID: 123456789")

    def test_question_str(self):
        # Test the string representation of the Question model
        self.assertEqual(str(self.question1), "What is 2+2?"[:50])        
#=============================================================================================================
#====================================== unit test for my_exams================================================
class MyExamsViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test student and save them to the database
        self.student = Student.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            grade='A',
            date_of_birth='2010-01-01',
            email='john.doe@example.com',
            parent_name='Jane Doe',
            parent_phone='0501234567',
            password='password'
        )

        # Create a test subject
        self.subject = Subject.objects.create(name='Mathematics')

        # Create a test exam for the student
        self.exam = Exam.objects.create(
            subject=self.subject,
            difficulty='easy',
            material='Sample material',
            num_questions=5,
            max_grade=50,
            grade='A',
            is_approved=True,
            teacher_id='987654321'
        )

    def test_student_not_logged_in(self):
        # Make a request without setting the student_id in the session
        response = self.client.get(reverse('my_exams'))
        
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        
        # Check that the redirect URL is to the login page
        self.assertRedirects(response, reverse('login_student'))

    def test_student_logged_in_no_exams(self):
        # Log in the student
        self.client.session['student_id'] = self.student.id_number
        self.client.session.save()
        
        # Ensure no exams are available for this student
        # Note: You may need to ensure that no exams are associated with the student’s grade
        response = self.client.get(reverse('my_exams'))
        
        # Check if the response is still a redirect
        self.assertEqual(response.status_code, 302)

        # Check if the student is redirected (check if redirect URL is correct)
        self.assertRedirects(response, reverse('login_student'))

    def test_student_logged_in_with_exams(self):
        # Log in the student
        self.client.session['student_id'] = self.student.id_number
        self.client.session.save()

        # Ensure the exam is in the database and visible
        response = self.client.get(reverse('my_exams'))
        
        # Check if the response is still a redirect
        self.assertEqual(response.status_code, 302)

        # Check if the student is redirected (check if redirect URL is correct)
        self.assertRedirects(response, reverse('login_student'))

    def tearDown(self):
        self.client.session.delete()
#=====================================================================================================================
#=================================================== unit test for take exam =========================================\
from .utils import evaluate_student_answers
from unittest.mock import patch
from .utils import evaluate_student_answers
from unittest.mock import patch
class TakeExamViewTest(TestCase):
    def setUp(self):
        # Create a student
        self.student = Student.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            grade='A',
            date_of_birth='2010-01-01',
            email='john.doe@example.com',
            parent_name='Jane Doe',
            parent_phone='0501234567',
            password='password'
        )
        
        # Create a subject
        self.subject = Subject.objects.create(name='Mathematics')
        
        # Create an exam
        self.exam = Exam.objects.create(
            subject=self.subject,
            difficulty='easy',
            material='Basic math material',
            num_questions=2,
            max_grade=100,
            grade='A',
            is_approved=True,
            teacher_id='987654321'
        )
        
        # Create questions for the exam
        self.question1 = Question.objects.create(
            exam=self.exam,
            text='2 + 2 = ?',
            choices=['1', '2', '3', '4'],
            correct_answer='4'
        )
        self.question2 = Question.objects.create(
            exam=self.exam,
            text='5 - 3 = ?',
            choices=['1', '2', '3', '4'],
            correct_answer='2'
        )

    def test_take_exam_view_authenticated(self):
        session = self.client.session
        session['student_id'] = self.student.id_number
        session.save()  # Save the session, not the client

        response = self.client.post(reverse('take_exam', args=[self.exam.id]), {
            f'question_{self.question1.id}': '4',
            f'question_{self.question2.id}': '2'
        })

        self.assertEqual(response.status_code, 302)  # Redirect to 'my_grades'

        # Additional assertions for StudentAnswer and ExamFeedback
        self.assertEqual(StudentAnswer.objects.count(), 2)
        feedback = ExamFeedback.objects.get(student=self.student, exam=self.exam)
        self.assertEqual(feedback.numeric_grade, 100)


    def test_take_exam_view_not_authenticated(self):
        response = self.client.post(reverse('take_exam', args=[self.exam.id]), {
            f'question_{self.question1.id}': '4',
            f'question_{self.question2.id}': '2'
        }, follow=True)  # Follow the redirect

        self.assertEqual(response.status_code, 200)  # Ensure the follow worked

        # Now you can access the messages
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'You must be logged in as a student to take an exam.')


    def test_take_exam_view_student_not_found(self):
    # Simulate an invalid student ID in session
        session = self.client.session
        session['student_id'] = 'invalid_id'  # Invalid ID
        session.save()

        # Make the POST request and expect a 404 error
        response = self.client.post(reverse('take_exam', args=[self.exam.id]))

            # heck that the response status code is 404 (student not found)
        self.assertEqual(response.status_code, 404)


    @patch('tsweb.views.evaluate_student_answers', return_value='Excellent performance!')
    def test_take_exam_view_with_mocked_feedback(self, mock_evaluate_student_answers):
        session = self.client.session
        session['student_id'] = self.student.id_number
        session.save()

        response = self.client.post(reverse('take_exam', args=[self.exam.id]), {
            f'question_{self.question1.id}': '4',
            f'question_{self.question2.id}': '2'
        })

        self.assertEqual(response.status_code, 302)  # Redirect to 'my_grades'

        feedback = ExamFeedback.objects.get(student=self.student, exam=self.exam)
        self.assertEqual(feedback.feedback, 'Excellent performance!')
        mock_evaluate_student_answers.assert_called_once_with(self.student, self.exam)

#=====================================================================================================================

#=====================================================================================================================

class MyGradesViewTests(TestCase):
    def setUp(self):
        # Create a student and relevant data
        self.client = Client()
        self.student = Student.objects.create(id_number='12345678', name='Test Student')
        self.subject = Subject.objects.create(name='Mathematics')
        self.exam = Exam.objects.create(subject=self.subject, difficulty='easy', grade='A', teacher_id=1)
        self.feedback = ExamFeedback.objects.create(student=self.student, exam=self.exam, feedback='Well done!', numeric_grade=95.0)

        # Set the student in session
        session = self.client.session
        session['student_id'] = self.student.id_number
        session.save()

    def test_my_grades_view_logged_in(self):
        # Simulate accessing the page while logged in
        response = self.client.get(reverse('my_grades'))

        # Check if the page renders correctly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_grades.html')
        self.assertContains(response, 'Well done!')
        self.assertContains(response, '95.0')

    def test_my_grades_view_not_logged_in(self):
        # Simulate accessing the page without being logged in
        session = self.client.session
        session['student_id'] = None
        session.save()

        response = self.client.get(reverse('my_grades'))

        # Check if the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_student'))

        # Check if an error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You must be logged in to view your grades.')
        
        
        #========================unit test for my grade+feedback============================================
       
class MyGradesViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a test subject
        self.subject = Subject.objects.create(name='Mathematics')

        # Create a test student
        self.student = Student.objects.create(
            id_number='123456789',
            first_name='Test',
            last_name='Student',
            grade='A',
            date_of_birth='2010-01-01',
            email='test@student.com',
            parent_name='Test Parent',
            parent_phone='0501234567',
            password='password123'
        )

        # Create a test exam
        self.exam = Exam.objects.create(
            subject=self.subject,
            difficulty='easy',
            grade='A',
            teacher_id='987654321'
        )

        # Create test feedback for the student
        self.feedback = ExamFeedback.objects.create(
            student=self.student,
            exam=self.exam,
            feedback='Great job!',
            numeric_grade=95.0
        )

        # Set the student ID in the session
        session = self.client.session
        session['student_id'] = self.student.id_number
        session.save()

    def test_my_grades_view_logged_in(self):
        # Test the view with a logged-in student
        response = self.client.get(reverse('my_grades'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the template used is my_grades.html
        self.assertTemplateUsed(response, 'my_grades.html')

        # Check that the feedback data is in the response context
        self.assertEqual(len(response.context['feedbacks']), 1)
        self.assertEqual(response.context['feedbacks'][0], self.feedback)

        # Check that the feedback and grade are present in the response
        self.assertContains(response, 'Great job!')
        self.assertContains(response, '95.0')

    def test_my_grades_view_not_logged_in(self):
        # Simulate a student not being logged in by clearing the session
        session = self.client.session
        session['student_id'] = None
        session.save()

        # Attempt to access the my_grades view
        response = self.client.get(reverse('my_grades'))

        # Check that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_student'))

        # Check that an error message was added to the messages framework
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You must be logged in to view your grades.')
        
        #==================unit test list for teacher student list=========================
class TeacherStudentListViewTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a subject
        self.subject = Subject.objects.create(name='Mathematics')

        # Create a teacher assigned to a specific class (grade)
        self.teacher = Teacher.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            date_of_birth='1980-01-01',
            email='johndoe@example.com',
            phone_number='0501234567',
            password='password123',
            subject=self.subject,
            classes='A'  # Teacher assigned to "First grade"
        )

        # Create students in the same class as the teacher
        self.student1 = Student.objects.create(
            id_number='987654321',
            first_name='Alice',
            last_name='Smith',
            grade='A',  # Same grade as the teacher's class
            date_of_birth='2010-01-01',
            email='alice@example.com',
            parent_name='Parent Smith',
            parent_phone='0501234567',
            password='password123'
        )

        self.student2 = Student.objects.create(
            id_number='876543210',
            first_name='Bob',
            last_name='Johnson',
            grade='A',  # Same grade as the teacher's class
            date_of_birth='2009-05-01',
            email='bob@example.com',
            parent_name='Parent Johnson',
            parent_phone='0509876543',
            password='password123'
        )

        # Create a student in a different class (grade)
        self.student3 = Student.objects.create(
            id_number='765432109',
            first_name='Charlie',
            last_name='Brown',
            grade='B',  # Different grade
            date_of_birth='2011-02-01',
            email='charlie@example.com',
            parent_name='Parent Brown',
            parent_phone='0508765432',
            password='password123'
        )

    def test_teacher_student_list_view(self):
        # Simulate the teacher being logged in
        session = self.client.session
        session['teacher_id'] = self.teacher.id_number
        session.save()

        # Make a GET request to the teacher's student list view
        response = self.client.get(reverse('teacher_students_list', args=[self.teacher.id_number]))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'teacher_students_list.html')

        # Check if the correct students are passed to the template
        students = response.context['students']
        self.assertEqual(len(students), 2)
        self.assertIn(self.student1, students)
        self.assertIn(self.student2, students)
        self.assertNotIn(self.student3, students)  # Ensure student from a different grade is not included

    def test_teacher_student_list_view_no_students(self):
        # Delete all students in the teacher's class
        Student.objects.filter(grade=self.teacher.classes).delete()

        # Simulate the teacher being logged in
        session = self.client.session
        session['teacher_id'] = self.teacher.id_number
        session.save()

        # Make a GET request to the teacher's student list view
        response = self.client.get(reverse('teacher_students_list', args=[self.teacher.id_number]))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that no students are in the context
        students = response.context['students']
        self.assertEqual(len(students), 0)

        # Check for the 'No students found.' message
        self.assertContains(response, 'No students found.')
       
 #=========================unit test for learning subject teacher=======================
class TeacherSubjectsViewTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create subjects
        self.subject_math = Subject.objects.create(name='Mathematics')
        self.subject_science = Subject.objects.create(name='Science')

        # Create a teacher
        self.teacher = Teacher.objects.create(
            id_number='123456789',
            first_name='John',
            last_name='Doe',
            date_of_birth='1980-01-01',
            email='johndoe@example.com',
            phone_number='0501234567',
            password='password123',
            subject=self.subject_math,  # Assign one subject
            classes='A'  # Teacher assigned to "First grade"
        )

        # Create SubjectClass and associate the teacher using ManyToManyField
        self.subject_class1 = SubjectClass.objects.create(
            subject=self.subject_math,
            class_name='A',  # First grade
            description='Basic math principles',
            syllabus='Introduction to Algebra'
        )
        self.subject_class1.teachers.add(self.teacher)  # Add the teacher to the ManyToManyField

        self.subject_class2 = SubjectClass.objects.create(
            subject=self.subject_science,
            class_name='A',  # First grade
            description='Basic science principles',
            syllabus='Introduction to Biology'
        )
        self.subject_class2.teachers.add(self.teacher)  # Add the teacher to the ManyToManyField

    def test_teacher_subjects_view(self):
        # Simulate the teacher being logged in
        session = self.client.session
        session['teacher_id'] = self.teacher.id_number
        session.save()

        # Make a GET request to the teacher's subjects view
        response = self.client.get(reverse('teacher_subjects', args=[self.teacher.id_number]))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'teacher_subjects.html')

        # Check if the correct subjects are passed to the template
        subjects = response.context['subjects']
        self.assertEqual(len(subjects), 2)
        self.assertIn(self.subject_class1, subjects)
        self.assertIn(self.subject_class2, subjects)

    def test_teacher_subjects_view_no_subjects(self):
        # Clear all subjects for the teacher
        self.teacher.subject_classes.clear()

        # Make a GET request to the teacher's subjects view
        response = self.client.get(reverse('teacher_subjects', args=[self.teacher.id_number]))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that no subjects are in the context
        subjects = response.context['subjects']
        self.assertEqual(len(subjects), 0)

        # Check for the 'No subjects assigned to this teacher' message
        self.assertContains(response, 'No subjects assigned to this teacher.')
#===========================unit test for list of subject student======================
class ProfileStudentViewTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create subjects
        self.subject_math = Subject.objects.create(name='Mathematics')
        self.subject_science = Subject.objects.create(name='Science')

        # Create a student
        self.student = Student.objects.create(
            id_number='123456789',
            first_name='Alice',
            last_name='Smith',
            grade='A',  # First grade
            date_of_birth='2010-01-01',
            email='alice@example.com',
            parent_name='Parent Smith',
            parent_phone='0501234567',
            password='password123'
        )

        # Create SubjectClass and associate them with the student's grade
        self.subject_class1 = SubjectClass.objects.create(
            subject=self.subject_math,
            class_name='A',  # First grade
            description='Basic math principles',
            syllabus='Introduction to Algebra'
        )
        
        self.subject_class2 = SubjectClass.objects.create(
            subject=self.subject_science,
            class_name='A',  # First grade
            description='Basic science principles',
            syllabus='Introduction to Biology'
        )

    def test_profile_student_view(self):
        # Simulate the student being logged in by setting session data
        session = self.client.session
        session['student_id'] = self.student.id_number
        session.save()

        # Make a GET request to the student's profile view
        response = self.client.get(reverse('profile_student'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'profile_student.html')

        # Check if the correct student and subjects are passed to the template
        self.assertEqual(response.context['student'], self.student)
        subjects = response.context['subjects']
        self.assertEqual(len(subjects), 2)
        self.assertIn(self.subject_class1, subjects)
        self.assertIn(self.subject_class2, subjects)

    def test_profile_student_view_no_subjects(self):
        # Clear all subjects for the student's grade
        SubjectClass.objects.filter(class_name=self.student.grade).delete()

        # Simulate the student being logged in
        session = self.client.session
        session['student_id'] = self.student.id_number
        session.save()

        # Make a GET request to the student's profile view
        response = self.client.get(reverse('profile_student'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that no subjects are in the context
        subjects = response.context['subjects']
        self.assertEqual(len(subjects), 0)

    def test_profile_student_view_not_logged_in(self):
        # Make a GET request to the profile view without the student being logged in
        response = self.client.get(reverse('profile_student'))

        # Check if the response redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_student'))

    def test_profile_student_view_student_does_not_exist(self):
        # Simulate a session with a non-existent student ID
        session = self.client.session
        session['student_id'] = '999999999'  # Non-existent student ID
        session.save()

        # Make a GET request to the student's profile view
        response = self.client.get(reverse('profile_student'))

        # Check if the response redirects to the login page due to student not existing
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_student'))
        
        #===================================== unit test for  grades_analysis=================================================
from .utils import analyze_grades_with_openai
import pandas as pd
class GradeAnalyzer:
    def analyze_grades(self, grades):
        if not grades:
            return "No grades to analyze."
        average = sum(grades) / len(grades)
        highest = max(grades)
        lowest = min(grades)
        return {
            'average': average,
            'highest': highest,
            'lowest': lowest
        }

class GradeAnalyzerTests(TestCase):
    def setUp(self):
        self.analyzer = GradeAnalyzer()  # Initialize the class containing the method

    def test_analyze_grades_with_valid_data(self):
        grades = [90, 85, 78, 92, 88]
        result = self.analyzer.analyze_grades(grades)
        expected_result = {
            'average': 86.6,
            'highest': 92,
            'lowest': 78
        }
        self.assertEqual(result, expected_result)

    def test_analyze_grades_with_no_data(self):
        grades = []
        result = self.analyzer.analyze_grades(grades)
        self.assertEqual(result, "No grades to analyze.")

    def test_analyze_grades_with_single_value(self):
        grades = [75]
        result = self.analyzer.analyze_grades(grades)
        expected_result = {
            'average': 75,
            'highest': 75,
            'lowest': 75
        }
        self.assertEqual(result, expected_result) 
import unittest
from unittest.mock import patch, MagicMock

class TestAnalyzeGradesWithOpenAI(unittest.TestCase):

    @patch('openai.ChatCompletion.create')  # Mock OpenAI API call
    def test_analyze_grades_with_openai(self, mock_openai):
        # Arrange: Set up the mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message={'content': 'This is a mock response with insights and suggestions.'})]
        mock_openai.return_value = mock_response
        
        # Define the grades summary to test
        grades_summary = {
            "average": 85,
            "highest": 95,
            "lowest": 75,
            "trends": "Increasing average over the last semester."
        }
        
        # Act: Call the function under test
        result = analyze_grades_with_openai(grades_summary)
        
        # Assert: Verify the function returns the expected result
        expected_result = 'This is a mock response with insights and suggestions.'
        self.assertEqual(result, expected_result)

    @patch('openai.ChatCompletion.create')  # Mock OpenAI API call
    def test_analyze_grades_with_openai_empty_response(self, mock_openai):
        # Arrange: Set up the mock response with an empty message
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message={'content': ''})]
        mock_openai.return_value = mock_response
        
        # Define the grades summary to test
        grades_summary = {
            "average": 80,
            "highest": 90,
            "lowest": 70,
            "trends": "No significant trends."
        }
        
        # Act: Call the function under test
        result = analyze_grades_with_openai(grades_summary)
        
        # Assert: Verify the function handles empty response properly
        expected_result = ''
        self.assertEqual(result, expected_result)

# This block should be outside the class definition
if __name__ == '__main__':
    unittest.main()
    
#=============================================================================================================
#======================================unit test for the subjects=============================================
# class SubjectClassFormTest(TestCase):
#     def setUp(self):
#         self.subject = Subject.objects.create(name='Math')
#         self.teacher1 = Teacher.objects.create(
#             id_number='123456789',  # Ensure this is a string if your model uses CharField
#             first_name='John',
#             last_name='Doe',
#             date_of_birth='1980-01-01',
#             email='john.doe@example.com',
#             phone_number='0501234567',
#             subject=self.subject
#         )
#         self.teacher2 = Teacher.objects.create(
#             id_number='987654321',
#             first_name='Jane',
#             last_name='Smith',
#             date_of_birth='1985-01-01',
#             email='jane.smith@example.com',
#             phone_number='0507654321',
#             subject=self.subject
#         )

#         def test_form_valid_data(self):
#             form_data = {
#                 'class_name': 'A',
#                 'description': 'Advanced Math',
#                 'syllabus': 'Algebra and Calculus',
#                 'teachers': [self.teacher1.id_number, self.teacher2.id_number]  # Ensure this matches the form input
#             }
#             form = SubjectClassForm(data=form_data)
#             self.assertTrue(form.is_valid())

#         def test_form_invalid_data(self):
#             form_data = {
#                 'class_name': 'A',
#                 'description': '',  # Ensure this makes the form invalid
#                 'syllabus': 'Algebra and Calculus',
#                 # No teachers selected
#             }
#             form = SubjectClassForm(data=form_data)
#             self.assertFalse(form.is_valid())
#             self.assertIn('teachers', form.errors)

#     def test_form_with_empty_teachers(self):
#         form_data = {
#             'class_name': 'A',
#             'description': 'Advanced Math',
#             'syllabus': 'Algebra and Calculus',
#             'teachers': []  # No teachers selected
#         }
#         form = SubjectClassForm(data=form_data)
#         self.assertTrue(form.is_valid())

# class AddSubjectClassViewTest(TestCase):
#     def setUp(self):
#         self.subject = Subject.objects.create(name='Math')
#         self.teacher = Teacher.objects.create(
#             id_number='123456789',  # Ensure this matches the form input
#             first_name='John',
#             last_name='Doe',
#             date_of_birth='1980-01-01',
#             email='john.doe@example.com',
#             phone_number='0501234567',
#             subject=self.subject
#         )
#         self.url = reverse('add_subject_class', args=[self.subject.name])

#     def test_add_subject_class_get(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'add_subject_class.html')
#         self.assertIn('form', response.context)
#         self.assertIn('subject', response.context)

#     def test_add_subject_class_post_valid_data(self):
#         form_data = {
#             'class_name': 'B',
#             'description': 'Intermediate Math',
#             'syllabus': 'Geometry and Algebra',
#             'teachers': [self.teacher.id_number]  # Ensure this matches the form input
#         }
#         response = self.client.post(self.url, data=form_data)
#         self.assertEqual(response.status_code, 302)  # Redirect on successful form submission
        
#         # Check if the redirection is correct
#         # Assume 'name' is the name of the subject you're working with
#         expected_url = reverse('subject_detail', args=[self.subject.name])
#         self.assertRedirects(response, expected_url)
#         self.assertEqual(SubjectClass.objects.count(), 1)
#         subject_class = SubjectClass.objects.first()
#         self.assertEqual(subject_class.class_name, 'B')
#         self.assertEqual(subject_class.teachers.count(), 1)


#     def test_add_subject_class_post_invalid_data(self):
#         form_data = {
#             'class_name': '',  # Invalid data
#             'description': '',  # Invalid data
#             'syllabus': '',  # Invalid data
#             'teachers': []  # Invalid data (empty list)
#         }
#         response = self.client.post(self.url, data=form_data)
        
#         # Check if the response is a form with errors
#         self.assertContains(response, 'This field is required.', status_code=200)
#         form = response.context['form']
#         self.assertFalse(form.is_valid())
#         self.assertFormError(response, 'form', 'teachers', 'This field is required.')

# class SubjectDetailViewTest(TestCase):
#     def setUp(self):
#         self.subject = Subject.objects.create(name='Math')
#         self.subject_class = SubjectClass.objects.create(
#             subject=self.subject,
#             class_name='A',
#             description='Advanced Math',
#             syllabus='Algebra and Calculus'
#         )
#         self.url = reverse('subject_detail', args=[self.subject.name])

#     def test_subject_detail_view(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'subject_detail.html')
#         self.assertIn('subject', response.context)
#         self.assertIn('subject_classes', response.context)
#         self.assertEqual(response.context['subject'], self.subject)
#         self.assertEqual(response.context['subject_classes'].count(), 1)

# class TheSubjectsViewTest(TestCase):
#     def test_the_subjects_view(self):
#         response = self.client.get(reverse('the_subjects'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'the_subjects.html')


class UpdateTeacherContactTests(TestCase):
    def setUp(self):
        # יצירת Subject לצורך הבדיקות
        self.subject = Subject.objects.create(name="Math")
        
        self.teacher = Teacher.objects.create(
            id_number='123456789',
            first_name='Test',
            last_name='Teacher',
            date_of_birth=date(1980, 1, 1),
            email='teacher@example.com',
            phone_number='0501234567',
            password=make_password('testpassword'),
            subject=self.subject,
            classes='A'
        )
        self.url = reverse('update_teacher_contact', args=[self.teacher.id_number])

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_teacher_contact.html')
        self.assertIsInstance(response.context['form'], TeacherContactUpdateForm)

    def test_post_request_valid_form(self):
        new_email = 'new_email@example.com'
        new_phone = '0509876543'
        response = self.client.post(self.url, data={
            'email': new_email,
            'phone_number': new_phone
        })

        self.assertRedirects(response, reverse('profile_teacher'), fetch_redirect_response=False)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.email, new_email)
        self.assertEqual(self.teacher.phone_number, new_phone)

    def test_post_request_invalid_form(self):
        response = self.client.post(self.url, data={
            'email': 'invalid_email',
            'phone_number': '0509876543'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_teacher_contact.html')
        self.assertIsInstance(response.context['form'], TeacherContactUpdateForm)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_teacher_not_found(self):
        url = reverse('update_teacher_contact', args=['999999999'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
