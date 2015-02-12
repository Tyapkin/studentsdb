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
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = [
        'last_name', 'first_name', 'middle_name', 'ticket', 'notes'
    ]

    form = StudentFormAdmin

    # def get_view_on_site_url(self, obj=None):
    #    return reverse('students_edit', kwargs={'pk': obj.pk})


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        """
        if the student is in another group, then the group
        can not be installed warden
        """
        # Set warning message
        warn_msg = u'Студент %s є учасником іншої групи.'

        if self.cleaned_data['leader'] is None:
            # Delete leader from group
            setattr(self.instance, 'leader', self.cleaned_data['leader'])
        elif self.cleaned_data['leader'].student_group != self.instance:
            raise ValidationError(warn_msg % (self.cleaned_data['leader']),
                                  code='invalid')

        return self.cleaned_data['leader']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    ordering = ['title']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']
    form = GroupFormAdmin

    # def get_view_on_site_url(self, obj=None):
    #    return reverse('groups_edit', kwargs={'pk': obj.pk})


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass

@admin.register(ExamResults)
class ExamResultsAdmin(admin.ModelAdmin):
    pass
