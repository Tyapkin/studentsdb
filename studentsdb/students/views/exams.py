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

    paginator = Paginator(exams, 5)
    page = request.GET.get('page')

    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        exams = paginator.page(1)
    except EmptyPage:
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exams.html', {'exams': exams})


def add_exam(request):
    return HttpResponse('<h1>Add exam</h1>')


def edit_exam(request, id):
    return HttpResponse('<h1>Edit exam %s</h1>' % id)


def delete_exam(request, id):
    return HttpResponse('<h1>Delete exam %s</h1>' % id)


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
