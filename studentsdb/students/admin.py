# coding=utf-8
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ValidationError, ModelForm

from .models.students import Student
from .models.groups import Group
from .models.exams import Exam, ExamResults


class StudentFormAdmin(ModelForm):
    def clean_student_group(self):
        """
        Check if student is leader in any group.
        If yes, then ensure it`s the same as selected group.
        """
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)

        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.',
                                  code='invalid')

        return self.cleaned_data['student_group']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'last_name', 'first_name', 'ticket', 'student_group'
    ]
    list_display_links = [
        'last_name', 'first_name'
    ]
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = [
        'last_name', 'first_name', 'middle_name', 'ticket', 'notes'
    ]

    form = StudentFormAdmin

    def get_view_on_site_url(self, obj=None):
        return reverse('students_edit', kwargs={'pk': obj.id})


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    ordering = ['title']
    list_editable = ['leader']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']

    def get_view_on_site_url(self, obj=None):
        return reverse('groups_edit', kwargs={'pk': obj.id})


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass

@admin.register(ExamResults)
class ExamResultsAdmin(admin.ModelAdmin):
    pass
