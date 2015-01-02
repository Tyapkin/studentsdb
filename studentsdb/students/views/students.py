# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.students import Student
from ..models.groups import Group


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


def students_add(request):
    # Якщо форма була запощена:
    if request.method == 'POST':
        # Якщо кнопка Скасувати була натиснута:
            # Повертаємо користувача до списку студентів
        # Якщо кнопка Додати була натиснута:
        if request.POST.get('add_button') is not None:
            # Перевіряємо дані на коректність та збираємо помилки
            errors = {}

            if not errors:
            # Якщо дані були введені некоректно:
                 # Віддаємо форму разом із знайденими помилками
            # Якщо дані були введенні коректно:
                # Створюємо та зберігаємо студента в базу
                student = Student(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    middle_name=request.POST['middle_name'],
                    birthday=request.POST['birthday'],
                    ticket=request.POST['ticket'],
                    student_group=
                        Group.objects.get(pk=request.POST['student_group']),
                    photo=request.FILES['photo'],
                )
                student.save()
                # Поретаємо користувача до списку студентів
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                     'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(reverse('home'))
    # Якщо форма не була запощена:
    else:
        # Поертаємо код початково стану форми
        groups = Group.objects.all().order_by('title')
        return render(request, 'students/students_add.html', {'groups': groups})


def students_edit(request, id):
    return HttpResponse('<h1>Student %s edit</h1>' % id)


def students_delete(request, id):
    return HttpResponse('<h1>Student %s delete</h1>' % id)
