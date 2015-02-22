# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from ..util import paginate
from ..models.students import Student
from ..forms.forms import StudentCreateForm, StudentUpdateForm


# Class based views for students
class StudentListView(TemplateView):
    template_name = 'students/students_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)

        # get variable 'order_by' from request.GET
        order_by = self.request.GET.get('order_by', '')
        # get queryset from Student
        students = Student.objects.all()

        # try to order students list
        if order_by in ('last_name', 'first_name', 'ticket'):
            students = students.order_by(order_by)

            # if reverse in request.GET
            if self.request.GET.get('reverse', '') == '1':
                # sort student list reverse
                students = students.reverse()
        else:
            students = students.order_by('last_name')


        context = paginate(students, 5, self.request, context,
                           var_name='students')

        return context


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = 'students/students_form.html'
    success_msg = u'Студент успішно доданий.'
    cancel_msg = u'Додавання студента скасовано.'

    def get_form_kwargs(self):
        kwargs = super(StudentCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            messages.warning(self.request, self.cancel_msg)
            return reverse('home')
        else:
            return super(StudentCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('home')


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_form.html'
    form_class = StudentUpdateForm
    success_msg = u'Студента успішно збережено'
    cancel_msg = u'Редагування студента скасовано'

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            messages.warning(self.request, self.cancel_msg)
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'
    success_msg = u'Студента успішно видалено.'

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('home')
