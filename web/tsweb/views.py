from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *

# Create your views here.

def home(request):
    return render(request, 'home.html',{})

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed successfully!")
            return redirect('login_student') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentSignUpForm()
    return render(request, 'signup_student.html', {'form': form})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed successfully!")
            return redirect('login_teacher')  # או לכל דף אחר שתרצה
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeacherSignUpForm()
    return render(request, 'teacher_signup.html', {'form': form})