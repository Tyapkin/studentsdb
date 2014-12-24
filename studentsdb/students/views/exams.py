# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

from ..models.exams import Exam, ExamResults


def exams_list(request):
    exams = Exam.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')

    if order_by in ('exam_name', 'date_exam', 'teacher', 'exam_group'):
        exams = exams.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    paginator = Paginator(exams, 3)
    page = request.GET.get('page')

    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        exams = paginator.page(1)
    except EmptyPage:
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exams.html', {'exams': exams})


def add_exam(request):
    pass


def edit_exam(request, eid):
    pass


def delete_exam(request, eid):
    pass


def exam_results(request, eid):
    # Переделать эту вьюху нахрен. Логика х*#$ня, выводит результаты совсем не
    # что ожидаешь.

    try:
        results = ExamResults.objects.filter(pk=eid)
    except ObjectDoesNotExist:
        raise Http404

    for r in results:
        print '%s | %s - %s' % (r.exam.exam_name, r.student, r.get_grade_display())

    return HttpResponse('Ok')
