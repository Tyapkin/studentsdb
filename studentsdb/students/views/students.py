# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.students import Student
from ..forms.forms import StudentCreateForm, StudentUpdateForm


# Views for students
def students_list(request):
    students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')

    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')

    # paginate students
    paginator = Paginator(students, 5)
    page = request.GET.get('page')

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html',
                  {'students': students})


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
