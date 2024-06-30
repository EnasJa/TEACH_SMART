from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('',views.home,name='home'),
  path('student_signup/', views.student_signup, name='student_signup'),
  path('login_student/', auth_views.LoginView.as_view(template_name='login_student.html'), name='login_student'),
  path('teacher_signup/', views.teacher_signup, name='teacher_signup'),
  path('login_teacher/', auth_views.LoginView.as_view(template_name='login_teacher.html'), name='login_teacher'),

]
