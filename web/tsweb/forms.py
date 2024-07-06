from datetime import date
from django import forms
from .models import *
from django.core.exceptions import ValidationError


class StudentSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=("Password"))
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=("Password verification"))

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
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if len(password) < 8:
                raise ValidationError(("The password must be at least 8 characters long."))
            if password != confirm_password:
                raise ValidationError(("The passwords do not match."))

        return cleaned_data
    
class TeacherSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=("Password"))
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=("Password verification"))

    class Meta:
        model = Teacher
        fields = ['id_number', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'password']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age < 21:
            raise ValidationError(("The teacher must be at least 21 years old."))
        elif age > 70:
            raise ValidationError(("The teacher's age is unusual. Please check the birthdate."))
        
        return dob

    def clean_email(self):
        email = self.cleaned_data['email']
        if Teacher.objects.filter(email=email).exists():
            raise ValidationError(("The email address already exists in the system."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if len(password) < 8:
                raise ValidationError(("The password must be at least 8 characters long."))
            if password != confirm_password:
                raise ValidationError(("The passwords do not match."))

        return cleaned_data