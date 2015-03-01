# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from ..util import paginate, get_current_group
from ..models.exams import Exam, ExamResults
from ..forms.forms import ExamEditForm, ExamCreateForm


class ExamListView(ListView):
    template_name = 'students/exams.html'
    model = Exam

    def get_queryset(self):
        current_group = get_current_group(self.request)

        if current_group:
            object_list = Exam.objects.filter(exam_group=current_group)
            print '<<< object_list ==>> ', object_list
        else:
            object_list = Exam.objects.order_by('exam_name')

        return object_list

    def get_context_data(self, **kwargs):
        context = super(ExamListView, self).get_context_data(**kwargs)

        order_by = self.request.GET.get('order_by', '')

        if order_by in ('exam_name', 'date_exam', 'teacher', 'exam_group',
                        'auditorium'):
            self.object_list = self.object_list.order_by(order_by)

            if self.request.GET.get('reverse', '') == '1':
                self.object_list = self.object_list.reverse()

        context = paginate(self.object_list, 5, self.request, context,
                           var_name='exam_list')

        return context


class ExamCreateView(CreateView):
    model = Exam
    template_name = 'students/exams_form.html'
    form_class = ExamCreateForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, u'Екзамен успішно додано.')
        return reverse('exams')


class ExamEditView(UpdateView):
    model = Exam
    template_name = 'students/exams_form.html'
    form_class = ExamEditForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            messages.warning(self.request, u'Редагування іспиту скасовано.')
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamEditView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, u'Зміни збережено успішно.')
        return reverse('exams')


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exam_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u'Екзамен успішно видалено.')
        return reverse('exams')


def exam_results(request, id):

    meta_data = {}

    try:
        results = ExamResults.objects.filter(exam_id=id)
    except ObjectDoesNotExist:
        raise Http404

    # meta_data is a dictionary wich contains group name and exam name
    meta_data['exam_name'] = results[0].exam.exam_name
    meta_data['group_name'] = results[0].exam.exam_group.title

    # try to order students list
    order_by = request.GET.get('order_by', '')

    if order_by in ('exam_name', 'student', 'grade'):
        results = results.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            results = results.reverse()

    return render(request, 'students/exam_results.html',
                  {'results': results, 'meta_data': meta_data})


def delete_exam_result(request, id):
    return HttpResponse('<h1>Delete exam %s result</h1>' % id)


def edit_exam_result(request, id):
    return HttpResponse('<h1>Edit exam %s result</h1>' % id)


"""
ProtectedError
Разобраться с єкзаменами...
реализовать удаление екзамена и его результатов.
"""
