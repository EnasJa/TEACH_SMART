from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404


from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import AdminLoginForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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

    
    subjects = SubjectClass.objects.filter(class_name=student.grade)
    return render(request, 'profile_student.html', {
        'student': student,
        'subjects': subjects})

# def logout_student(request):
#     return render(request, 'home.html')

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
                    request.session['teacher_id'] = teacher.id_number
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


def listof_student (request):
    soft=Student.objects.all()
    return render(request,'listof_student.html')

# def profile_teacher(request):
#        return render(request, 'profile_teacher.html',{})
def profile_teacher(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('login_teacher')
    print(teacher_id)
    try:
        teacher = Teacher.objects.get(id_number=teacher_id)
    except Teacher.DoesNotExist:
        messages.error(request, 'teacher not found')
        return redirect('login_teacher')
    return render(request, 'profile_teacher.html', {'teacher': teacher})

# def logout_teacher(request):
#     return render(request, 'home.html')


def teacher_students_list(request, id_number):
    teacher = get_object_or_404(Teacher, id_number=id_number)
    students = Student.objects.filter(grade=teacher.classes).distinct()
    return render(request, 'teacher_students_list.html', {'teacher': teacher, 'students': students})
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


# def logout_admin(request):
#     if 'admin_user_id' in request.session:
#         del request.session['admin_user_id']
#     return redirect('login_admin')



def the_subjects(request):
    return render(request, 'the_subjects.html')
def subject_detail(request, name):
    subject = get_object_or_404(Subject, name=name)
    subject_classes = subject.subject_classes.all()  # Access related classes
    return render(request, 'subject_detail.html', {'subject': subject, 'subject_classes': subject_classes})
def add_subject_class(request, name):
    subject = get_object_or_404(Subject, name=name)
    teachers = Teacher.objects.filter(subject=subject)
    
    if request.method == 'POST':
        form = SubjectClassForm(request.POST)
        if form.is_valid():
            # Handle form submission
            subject_class = form.save(commit=False)
            subject_class.subject = subject
            subject_class.save()
            # Redirect or handle success
    else:
        form = SubjectClassForm()
        form.fields['teachers'].queryset = teachers
    
    return render(request, 'add_subject_class.html', {'form': form, 'subject': subject})



def about_us(request):
    return render(request, 'about_us.html')


def teacher_subjects(request, teacher_id):
    # Fetch the teacher based on the ID
    teacher = get_object_or_404(Teacher, id_number=teacher_id)
    
    # Get the subjects the teacher is teaching
    subjects = teacher.subject_classes.all()
    
    return render(request, 'teacher_subjects.html', {
        'teacher': teacher,
        'subjects': subjects
    })
 


def add_teacher(request):
    if request.method == 'POST':
        form = addTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed successfully!")
            return redirect('teacher_list')  # או לכל דף אחר שתרצה
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = addTeacherForm()
    return render(request, 'add_teacher.html', {'form': form})



def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})


# def delete_teacher(request, id):
#     obj =Teacher.objects.get(pk=id)
#     obj.delete()
#     return redirect('teacher_list')

def search_teacher(request):
    if request.method=="POST":
        searched=request.POST['searched']
        searched = Teacher.objects.filter(first_name__icontains=searched)
        if not searched:
            messages.success(request, "The teacher does not exist.")
            return render(request, 'search_teacher.html', {})
        else:

           return render(request, 'search_teacher.html', {'searched':searched})

    else:
        return render(request, 'search_teacher.html', {})


def delete_teacher(request, id_number):
    teacher = get_object_or_404(Teacher, id_number=id_number)

    if request.method == 'POST':
        teacher.delete()
        messages.success(request, f'the teacher {teacher.first_name} {teacher.last_name} deleted successfully.')
        return redirect('teacher_list')
    return render(request, 'confirm_delete_teacher.html', {'teacher': teacher})



# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# bot =ChatBot('chatbot',read_only = False, logic_adapters =
#              [
#                 {
#                     'import_path':'chatterbot.logic.BestMatch',
#                     # 'default_response':'Sorry, I dont Know what that means',
#                     # 'maximum_similarity_threshold':0.90,
               
#                }
#               ])
# list_to_train=[
#     "hi",
#     "hi there",
#     "whats your name ",
#     "im just chat bot",
#      "what your fav food ",
#     "i like cheese",
# ]
# # list_trainer=ListTrainer(bot)

# # list_trainer.train(list_to_train)


# # ChatterBotCorpusTrainer=ChatterBotCorpusTrainer(bot)
# # ChatterBotCorpusTrainer.train('chatterbot.corpus.english')


# # Create a ChatterBotCorpusTrainer instance and train with the English corpus
# corpus_trainer = ChatterBotCorpusTrainer(bot)
# corpus_trainer.train('chatterbot.corpus.english')

# def chatbot(request):
#     return render(request,'chatbot.html')

# def getResponse(request):
#     userMessage =request.GET.get('userMessage')
#     chat_response=str(bot.get_response(userMessage))
#     print(chat_response)
#     return HttpResponse(chat_response)



# def getResponse(request):
#     user_message = request.GET.get('userMessage', '')
#     # Process the user_message and generate a response
#     bot_response = "This is a placeholder response."
#     return HttpResponse(bot_response)


def logout_student(request):
    if request.method == 'POST':
        # Check if the user confirmed the logout
        if request.POST.get('confirm_logout'):
            logout(request)
            return redirect('home')
        else:
            # Redirect back to the student profile page
            return redirect('profile_student')
    else:
        # Render the logout page with the confirmation modal
        return render(request, 'logout.html', {'user_type': 'student'})

def logout_teacher(request):
    if request.method == 'POST':
        # Check if the user confirmed the logout
        if request.POST.get('confirm_logout'):
            logout(request)
            return redirect('home')
        else:
            # Redirect back to the teacher profile page
            return redirect('profile_teacher')
    else:
        # Render the logout page with the confirmation modal
        return render(request, 'logout.html', {'user_type': 'teacher'})
    


def logout_admin(request):
    # if 'admin_user_id' in request.session:
    #     del request.session['admin_user_id']
    # return redirect('login_admin')
    if request.method == 'POST':
        # Check if the user confirmed the logout
        if request.POST.get('confirm_logout'):
            logout(request)
            return redirect('home')
        else:
            # Redirect back to the teacher profile page
            return redirect('admin_homepage')
    else:
        # Render the logout page with the confirmation modal
        return render(request, 'logout.html', {'user_type': 'admin'})
