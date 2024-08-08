from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView



urlpatterns = [
  path('',views.home,name='home'),
  path('LogIn/', views.LogIn, name='LogIn'),
  path('logout_student/', views.logout_student, name='logout_student'),
  path('logout_teacher/', views.logout_teacher, name='logout_teacher'),
  path('student_signup/', views.student_signup, name='student_signup'),
  path('profile_student/', views.profile_student, name='profile_student'),
  path('login_teacher/', views.login_teacher, name='login_teacher'),
  path('profile_teacher/', views.profile_teacher, name='profile_teacher'),
  path('teacher/<str:id_number>/students/', views.teacher_students_list, name='teacher_students_list'),
  path('login_student/', views.login_student, name='login_student'),
  path('teacher_signup/', views.teacher_signup, name='teacher_signup'),
  path('send/', views.send_message, name='send_message'),
  path('inbox/', views.inbox, name='inbox'),
  path('message-sent/', views.message_sent, name='message_sent'),
  path('login_student/', auth_views.LoginView.as_view(template_name='login_student.html'), name='login'),
  path('login_admin/', views.login_admin, name='login_admin'),
  path('admin_homepage/', views.admin_homepage, name='admin_homepage'),
  path('logout_admin/',views.logout_admin, name="logout_admin"), #admin logout
  path('the_subjects/', views.the_subjects, name='the_subjects'),
   path('subject_detail/<str:name>/', views.subject_detail, name='subject_detail'),
    path('add_subject_class/<str:name>/', views.add_subject_class, name='add_subject_class'),
  path('add_teacher/',views.add_teacher, name="add_teacher"), 
  path('teacher_list/',views.teacher_list, name="teacher_list"),
  path('search_teacher/',views.search_teacher, name="search_teacher"),


  path('about_us/', views.about_us, name='about_us'),
  path('teacher_subjects/<int:teacher_id>/', views.teacher_subjects, name='teacher_subjects'),
  

  path('delete_teacher/<str:id_number>/', views.delete_teacher, name='delete_teacher'),
  path('chatbot/', views.chatbot, name='chatbot'),
  path('getResponse',views.getResponse,name='getResponse')
]

