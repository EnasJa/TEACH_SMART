from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from requests import session
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
import random


from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import AdminLoginForm, addStudentForm
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

    admin = Admin.objects.get(Username="admin")

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
    teacher_id = request.session.get('teacher_id')
    # print(student_id)
    try:
        teacher = Teacher.objects.get(id_number=teacher_id)
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


import os
def login_teacher(request):
    print("Request method:", request.method)  # Debug print statement
    if request.method == 'POST':
        print(os.getenv("OPENAI_API_KEY"))
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
            except Teacher.DoesNotExist:  # Catch Teacher.DoesNotExist, not Student.DoesNotExist
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
#--------------------------------- SPRINT 2-------------------------------------------

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

def add_student(request):
    if request.method == 'POST':
        form = addStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed successfully!")
            return redirect('student_list')  # או לכל דף אחר שתרצה
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = addStudentForm()
    return render(request, 'add_student.html', {'form': form})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})






########################chatbot#############################################
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
# list_trainer=ListTrainer(bot)

# # list_trainer.train(list_to_train)


# # ChatterBotCorpusTrainer=ChatterBotCorpusTrainer(bot)
# # ChatterBotCorpusTrainer.train('chatterbot.corpus.english')


# # Create a ChatterBotCorpusTrainer instance and train with the English corpus
# Create a ChatterBotCorpusTrainer instance and train with the English corpus
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

#-----------------------------HACKTON----------------------------------------------
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
    

#----------------------------------  SPRINT 3 -----------------------------------------------------
from .utils import generate_questions  # Ensure this function is defined

def create_exam(request):
    if request.method == 'POST':
        teacher_id = request.session.get('teacher_id')
        if not teacher_id:
            messages.error(request, 'You must be logged in to create an exam.')
            return redirect('login_teacher')
        
        try:
            teacher = Teacher.objects.get(id_number=teacher_id)
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher profile not found.')
            return redirect('login_teacher')
        
        # Pass the teacher instance to the form
        exam_form = ExamForm(request.POST, teacher=teacher)
        if exam_form.is_valid():
            exam = exam_form.save(commit=False)
            exam.teacher_id = teacher_id  # Explicitly set teacher_id
            exam.save()
            
            # Generate questions
            questions = generate_questions(exam)
            for q in questions:
                Question.objects.create(
                    exam=exam,
                    text=q['text'],
                    choices=q['choices'],
                    correct_answer=q['correct_answer'],
                )

            # Redirect to the review page
            return redirect('review_exam', pk=exam.pk)
    else:
        teacher_id = request.session.get('teacher_id')
        if not teacher_id:
            messages.error(request, 'You must be logged in to create an exam.')
            return redirect('login_teacher')
        
        try:
            teacher = Teacher.objects.get(id_number=teacher_id)
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher profile not found.')
            return redirect('login_teacher')
        
        # Create an empty form with the teacher context
        exam_form = ExamForm(teacher=teacher)

    return render(request, 'create_exam.html', {'form': exam_form})


def review_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    
    if request.method == 'POST':
        approved_question_ids = request.POST.getlist('approved_questions')
        
        for question in exam.question_set.all():  # Corrected to use question_set.all()
            if str(question.id) in approved_question_ids:
                question.is_approved = True  # Assuming you have an `is_approved` field in your Question model
            else:
                question.is_approved = False
            question.save()
        
        # Check if all questions are approved
        if all(q.is_approved for q in exam.question_set.all()):
            exam.is_approved = True
            messages.success(request, 'All questions approved. Exam approved successfully!')
        else:
            exam.is_approved = False
            messages.warning(request, 'Not all questions were approved. Please review the questions.')
        
        exam.save()
        return redirect('profile_teacher')  # Redirect to a relevant page

    return render(request, 'review_exam.html', {'exam': exam})

def my_exams(request):
    student_id = request.session.get('student_id')
    if not student_id:
        messages.error(request, 'You must be logged in to view your exams.')
        return redirect('login_student')

    student = get_object_or_404(Student, id_number=student_id)
    exams = Exam.objects.filter(grade=student.grade, is_approved=True)
    return render(request, 'my_exams.html', {'exams': exams})


    
from .utils import evaluate_student_answers
def take_exam(request, exam_id):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, 'You must be logged in as a student to take an exam.')
        return redirect('login_student')

    try:
        student = get_object_or_404(Student, id_number=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'No matching student found. Please log in again.')
        return redirect('login_student')
    
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Question.objects.filter(exam=exam).order_by('id')
    
    if request.method == 'POST':
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            is_correct = selected_answer == question.correct_answer

            if is_correct:
                correct_answers += 1

            StudentAnswer.objects.create(
                student=student,
                exam=exam,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct
            )

        numeric_grade = (correct_answers / total_questions) * exam.max_grade

        # Get feedback from AI
        feedback = evaluate_student_answers(student, exam)

        # Save the feedback to the database
        ExamFeedback.objects.update_or_create(
            student=student,
            exam=exam,
            defaults={'numeric_grade': numeric_grade, 'feedback': feedback}
        )

        messages.success(request, f'Your exam is submitted successfully! Your grade is {numeric_grade:.2f}.')
        return redirect('my_grades')

    return render(request, 'take_exam.html', {'exam': exam, 'questions': questions})
def my_grades(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, 'You must be logged in to view your grades.')
        return redirect('login_student')

    # Fetch the student
    student = get_object_or_404(Student, id_number=student_id)

    # Retrieve feedback for the student
    feedbacks = ExamFeedback.objects.filter(student=student)

    return render(request, 'my_grades.html', {'feedbacks': feedbacks})
import pandas as pd

from .utils import analyze_grades_with_openai  # Ensure this function is defined

def grades_analysis(request):
    # Check if the user is a teacher in the session
    teacher_id = request.session.get('teacher_id')
    
    if not teacher_id:
        messages.error(request, 'You must be a teacher to access this page.')
        return redirect('login_teacher')  # Redirect to teacher login or another page if not a teacher

    # Fetch teacher object from database
    teacher = get_object_or_404(Teacher, id_number=teacher_id)

    # Fetch feedbacks associated with the teacher's exams using teacher_id
    feedbacks = ExamFeedback.objects.filter(exam__teacher_id=teacher_id)
    
    if feedbacks.exists():
        # Prepare data for analysis
        data = feedbacks.values('numeric_grade', 'exam__subject__name')
        df = pd.DataFrame(list(data))
        
        # Summarize the data
        analysis = df.groupby('exam__subject__name')['numeric_grade'].agg(['mean', 'std', 'max', 'min']).reset_index()
        grades_summary = analysis.to_string(index=False)
        
        # Get insights from OpenAI
        insights = analyze_grades_with_openai(grades_summary)
    else:
        insights = "No exam feedbacks available for analysis."

    return render(request, 'grades_analysis.html', {'insights': insights})
# def grades_analysis(request):
#     # Check if the user is a teacher in the session
#     teacher_id = request.session.get('teacher_id')
    
#     if not teacher_id:
#         messages.error(request, 'You must be a teacher to access this page.')
#         return redirect('login_teacher')  # Redirect to teacher login or another page if not a teacher

#     # Fetch teacher object from database
#     teacher = get_object_or_404(Teacher, id_number=teacher_id)

#     # Fetch feedbacks associated with all exams taken by the teacher
#     feedbacks = ExamFeedback.objects.filter(exam__teacher_id=teacher_id)
    
#     if feedbacks.exists():
#         # Organize feedbacks by exam
#         exams_feedback = feedbacks.values('exam__id', 'exam__subject__name', 'numeric_grade')
        
#         # Prepare data structure for analysis
#         exam_data = {}
#         for feedback in exams_feedback:
#             exam_id = feedback['exam__id']
#             subject_name = feedback['exam__subject__name']
#             grade = feedback['numeric_grade']
            
#             if exam_id not in exam_data:
#                 exam_data[exam_id] = {'subject_name': subject_name, 'grades': []}
            
#             exam_data[exam_id]['grades'].append(grade)
        
#         # Analyze each exam's feedback
#         analysis_results = []
#         for exam_id, data in exam_data.items():
#             df = pd.DataFrame(data['grades'], columns=['numeric_grade'])
            
#             # Summarize the data
#             analysis = df['numeric_grade'].agg(['mean', 'std', 'max', 'min'])
#             grades_summary = analysis.to_frame().reset_index()
#             grades_summary.columns = ['Metric', 'Value']
            
#             # Get insights from OpenAI or another analysis tool
#             insights = analyze_grades_with_openai(grades_summary.to_string(index=False))
            
#             analysis_results.append({
#                 'subject_name': data['subject_name'],
#                 'analysis': analysis,
#                 'insights': insights
#             })
#     else:
#         analysis_results = "No exam feedbacks available for analysis."

#     return render(request, 'grades_analysis.html', {'analysis_results': analysis_results})


def delete_student(request, id_number):
    student = get_object_or_404(Student, id_number=id_number)

    if request.method == 'POST':
        student.delete()
        messages.success(request, f'the student {student.first_name} {student.last_name} deleted successfully.')
        return redirect('students_list')
    return render(request, 'confirm_delete_student.html', {'student': student})



# @login_required
def update_teacher_contact(request, teacher_id):
    print("View is called!")
    teacher = get_object_or_404(Teacher, id_number=teacher_id)
    print(f"Teacher found: {teacher}")
    
    if request.method == 'POST':
        form = TeacherContactUpdateForm(request.POST, instance=teacher)
        print(f"Form is valid: {form.is_valid()}")  # בדוק אם הטופס תקין
        if form.is_valid():
            updated_teacher = form.save()
            print(f"Updated teacher: {updated_teacher.email}, {updated_teacher.phone_number}")  # בדוק את הערכים המעודכנים
            return redirect('profile_teacher')
        else:
            print(f"Form errors: {form.errors}")  # הדפס את השגיאות בטופס
    else:
        form = TeacherContactUpdateForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
    }
    return render(request, 'update_teacher_contact.html', context)
