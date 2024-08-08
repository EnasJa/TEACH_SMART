from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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




def delete_teacher(request, id_number):
    teacher = get_object_or_404(Teacher, id_number=id_number)

    if request.method == 'POST':
        teacher.delete()
        messages.success(request, f'the teacher {teacher.first_name} {teacher.last_name} deleted successfully.')
        return redirect('teacher_list')
    return render(request, 'confirm_delete_teacher.html', {'teacher': teacher})



from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

bot =ChatBot('chatbot',read_only = False, logic_adapters =
             [
                {
                    'import_path':'chatterbot.logic.BestMatch',
                    # 'default_response':'Sorry, I dont Know what that means',
                    # 'maximum_similarity_threshold':0.90,
               
               }
              ])
list_to_train=[
    "hi",
    "hi there",
    "whats your name ",
    "im just chat bot",
     "what your fav food ",
    "i like cheese",
]
# list_trainer=ListTrainer(bot)

# list_trainer.train(list_to_train)


# ChatterBotCorpusTrainer=ChatterBotCorpusTrainer(bot)
# ChatterBotCorpusTrainer.train('chatterbot.corpus.english')


# Create a ChatterBotCorpusTrainer instance and train with the English corpus
corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english')

def chatbot(request):
    return render(request,'chatbot.html')

def getResponse(request):
    userMessage =request.GET.get('userMessage')
    chat_response=str(bot.get_response(userMessage))
    print(chat_response)
    return HttpResponse(chat_response)



# def getResponse(request):
#     user_message = request.GET.get('userMessage', '')
#     # Process the user_message and generate a response
#     bot_response = "This is a placeholder response."
#     return HttpResponse(bot_response)