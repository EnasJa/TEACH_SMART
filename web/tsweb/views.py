from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout


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


def send_message(request):
    # # נניח שיש לך מנגנון אימות מותאם אישית ששומר את ה-username של האדמין ב-session
    # admin_username = request.session.get('admin_username')
    
    # try:
    #     admin = Admin.objects.get(username=admin_username)
    # except Admin.DoesNotExist:
    #     raise PermissionDenied("Only admins can send messages.")

    admin = Admin.objects.get(username="SABA")

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = admin
            #admin
            message.save()
            form.save_m2m()
            return redirect('message_sent')
    else:
        form = MessageForm()
    
    return render(request, 'send_message.html', {'form': form})

def inbox(request):
    # נניח שיש לך מנגנון אימות מותאם אישית ששומר את ה-id_number של המורה ב-session
    # teacher_id = request.session.get('teacher_id')
    
    try:
        teacher = Teacher.objects.get(id_number=123454675)
        messages = teacher.received_messages.all().order_by('-created_at')
    except Teacher.DoesNotExist:
        raise PermissionDenied("Only teachers can view their inbox.")
    
    return render(request, 'inbox.html', {'messages': messages})


def message_sent(request):
    messages.success(request, 'ההודעה נשלחה בהצלחה!')
    return render(request, 'message_sent.html')

def login_student(request):
    print("Request method:", request.method)  # Debug print statement
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():  # Validate form data
            print("Form is valid")  # Debug print statement
            # Access cleaned data
            id_number = form.cleaned_data['id_number']
            password = form.cleaned_data['password']
            try:
                student = Student.objects.get(id_number=id_number)
                if check_password(password, student.password):
                    messages.success(request, 'Login successful')
                    # Log the user in
                    request.session['student_id'] = student.id_number
                    return redirect('profile_student')
                else:
                    messages.error(request, 'Invalid password')
                    print("Invalid password")  # Debug print statement
            except Student.DoesNotExist:
                messages.error(request, 'Invalid ID number')
                print("Invalid ID number")  # Debug print statement
        else:
            print("Form is not valid")  # Debug print statement
            print(form.errors)  # Print form errors
    else:
        form = StudentLoginForm()

    return render(request, 'login_student.html', {'form': form})


def profile_student(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login_student')

    try:
        student = Student.objects.get(id_number=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'Student not found')
        return redirect('login_student')

    return render(request, 'profile_student.html', {'student': student})

def logout_student(request):
    return render(request, 'home.html')

def LogIn(request):
    return render(request, 'LogIn.html')



def login_teacher(request):
    print("Request method:", request.method)  # Debug print statement
    if request.method == 'POST':
        form = loginTeacherForm(request.POST)
        if form.is_valid():  # Validate form data
            print("Form is valid")  # Debug print statement
            # Access cleaned data
            id_number = form.cleaned_data['id_number']
            password = form.cleaned_data['password']
            try:
                teacher = Teacher.objects.get(id_number=id_number)
                if check_password(password, teacher.password):
                    messages.success(request, 'Login successful')
                    # Log the user in
                    request.session['teacher_id'] = teacher.id
                    return redirect('profile_teacher')
                else:
                    messages.error(request, 'Invalid password')
                    print("Invalid password")  # Debug print statement
            except Student.DoesNotExist:
                messages.error(request, 'Invalid ID number')
                print("Invalid ID number")  # Debug print statement
        else:
            print("Form is not valid")  # Debug print statement
            print(form.errors)  # Print form errors
    else:
        form = loginTeacherForm()

    return render(request, 'login_teacher.html', {'form': form})


@login_required
def profile_teacher(request):
    return render(request, 'profile_teacher.html')


def listof_student (request):
    soft=Student.objects.all()
    return render(request,'listof_student.html')
#  ,{'soft':soft}
