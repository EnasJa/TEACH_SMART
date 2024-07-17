from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import AdminLoginForm
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'home.html',{})

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed successfully!")
            return redirect('login') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentSignUpForm()
    return render(request, 'signup_student.html', {'form': form})

def signup_success (request):
    return render(request, 'signup_success.html',{})


######################################################################33
#asia

def login_admin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username,password)
            try:
                user = Admin.objects.get(Username=username)
                if user.Password == password:
                # if user.check_password(password):
                    print("anfal")
                    # login(request, user)
                    request.session['user_id'] = user.id  # Example usage of session

                    return redirect(admin_homepage)
                else:
                    messages.error(request, 'Invalid username or password')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password')
            return redirect('login_admin')
    else:
        form = AdminLoginForm()
    return render(request, 'login_admin.html', {'form': form})





# @login_required
def admin_homepage(request):
    return render(request, 'admin_homepage.html')






