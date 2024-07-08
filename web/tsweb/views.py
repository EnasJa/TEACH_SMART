from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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