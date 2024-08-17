from datetime import date
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



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
    
class MessageForm(forms.ModelForm):
    all_teachers = forms.BooleanField(required=False, label='Send to all teachers')

    class Meta:
        model = Message
        fields = ['subject', 'content', 'recipients']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipients'].queryset = Teacher.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        all_teachers = cleaned_data.get('all_teachers')
        recipients = cleaned_data.get('recipients')

        if all_teachers:
            cleaned_data['recipients'] = Teacher.objects.all()
        elif not recipients:
            raise forms.ValidationError("You must select at least one recipient or choose 'Send to all teachers.")

        return cleaned_data

# login form
class StudentLoginForm(forms.Form):
    id_number = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'placeholder': 'id_number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class loginTeacherForm(forms.Form):
    id_number = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'placeholder': 'id_number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class SubjectClassForm(forms.ModelForm):
    class Meta:
        model = SubjectClass
        fields = ['class_name', 'description', 'syllabus', 'teachers']
    
    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.none(),  # Initialize with an empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
class addTeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=("Password"))
    # confirm_password = forms.CharField(widget=forms.PasswordInput, label=("Password verification"))

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
#=============================SPRINT 3===================================
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'difficulty', 'material', 'num_questions', 'max_grade', 'grade']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)  # Pass teacher object to form
        super().__init__(*args, **kwargs)

        if teacher:
            # Get the classes that the teacher handles
            teacher_classes = SubjectClass.objects.filter(teachers=teacher).values_list('class_name', flat=True)
            
            # Get subjects for the classes the teacher handles
            subjects = SubjectClass.objects.filter(class_name__in=teacher_classes).values_list('subject', 'subject__name')
            
            self.fields['subject'].queryset = Subject.objects.filter(id__in=[subject[0] for subject in subjects])
            
            # Filter grades based on the teacher's classes
            self.fields['grade'].choices = [(grade, dict(Exam.GRADE_CHOICES)[grade]) for grade in teacher_classes]
        else:
            # Default behavior if no teacher provided (optional)
            self.fields['subject'].queryset = Subject.objects.all()
            self.fields['grade'].choices = Exam.GRADE_CHOICES