from datetime import date
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class StudentSignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id_number', 'first_name', 'last_name', 'grade', 'date_of_birth', 'email', 'parent_name', 'parent_phone']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age < 7:
            raise ValidationError("The student must be at least 7 years old.")
        elif age > 12:
            raise ValidationError("The student must be no older than 12 years old.")        
        return dob


    def clean_email(self):
        email = self.cleaned_data['email']
        if Student.objects.filter(email=email).exists():
            raise ValidationError("The email address already exists in the system.")
        return email

    def clean_parent_phone(self):
        phone = self.cleaned_data['parent_phone']
        if not phone.startswith(('05')):
            raise ValidationError("A phone number must start with 05 .")
        return phone





##############################################################3
#asia
# class adminRegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
