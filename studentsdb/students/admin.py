from django.contrib import admin

from .models.students import Student
from .models.groups import Group
from .models.exams import Exam, ExamResults


@admin.register(Student, Exam, ExamResults)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


class ExamAdmin(admin.ModelAdmin):
    pass


class ExamResultsAdmin(admin.ModelAdmin):
    pass
