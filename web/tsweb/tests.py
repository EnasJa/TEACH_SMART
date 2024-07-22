from django.forms import ValidationError
from django.test import TestCase
from .models import Admin

class AdminModelTests(TestCase):
    
    def setUp(self):
        # Set up initial data or objects needed for the tests
        self.valid_admin_data = {
            'Username': 'asia',
            'Password': '123123'
        }

    def test_valid_username(self):
        # Test case for valid username
        admin = Admin(**self.valid_admin_data)
        try:
            admin.full_clean()
        except ValidationError as e:
            self.fail(f"Validation error: {e}")

    def test_valid_password(self):
        # Test case for valid password
        admin = Admin(**self.valid_admin_data)
        try:
            admin.full_clean()
        except ValidationError as e:
            self.fail(f"Validation error: {e}")

    def test_invalid_username(self):
        # Test case for invalid username
        invalid_admin_data = self.valid_admin_data.copy()
        invalid_admin_data['Username'] = ''  # Invalid username
        admin = Admin(**invalid_admin_data)
        with self.assertRaises(ValidationError):
            admin.full_clean()

    def test_invalid_password(self):
        # Test case for invalid password
        invalid_admin_data = self.valid_admin_data.copy()
        invalid_admin_data['Password'] = ''  # Invalid password
        admin = Admin(**invalid_admin_data)
        with self.assertRaises(ValidationError):
            admin.full_clean()
