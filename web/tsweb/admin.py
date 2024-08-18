from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Message)
# #------- SPRINT 2 ----------
admin.site.register(Subject)
admin.site.register(SubjectClass)
#------- SPRINT 3 ----------
admin.site.register(Exam)
admin.site.register(Question)


