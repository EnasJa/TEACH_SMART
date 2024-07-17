from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('',views.home,name='home'),
  path('student_signup/', views.student_signup, name='student_signup'),
  path('login_student/', auth_views.LoginView.as_view(template_name='login_student.html'), name='login'),
  path('login_admin/', views.login_admin, name='login_admin'),
  path('admin_homepage/', views.admin_homepage, name='admin_homepage'),

]
