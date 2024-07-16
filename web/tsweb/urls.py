from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
  path('',views.home,name='home'),
  path('LogIn/', views.LogIn, name='LogIn'),
  path('logout_student/', views.logout_student, name='logout_student'),
  path('student_signup/', views.student_signup, name='student_signup'),
 path('profile_student/', views.profile_student, name='profile_student'),
  path('login_student/', views.login_student, name='login_student'),
  path('teacher_signup/', views.teacher_signup, name='teacher_signup'),
  path('login_teacher/', auth_views.LoginView.as_view(template_name='login_teacher.html'), name='login_teacher'),
  path('send/', views.send_message, name='send_message'),
  path('inbox/', views.inbox, name='inbox'),
  path('message-sent/', views.message_sent, name='message_sent'),

]
