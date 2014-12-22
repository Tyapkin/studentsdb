from django.contrib import admin

from .models.students import Student
from .models.groups import Group
from .models.exams import Exam, ExamResults

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Exam)
admin.site.register(ExamResults)
