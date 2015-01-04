# -*- coding: utf-8 -*-
from datetime import datetime
from PIL import Image
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
    groups = Group.objects.all().order_by('title')
    # Якщо форма була запощена:
    if request.method == 'POST':
        # Якщо кнопка Додати була натиснута:
        if request.POST.get('add_button') is not None:
            # Перевіряємо дані на коректність та збираємо помилки
            errors = {}

            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u'Ім’я є обов’язковим'
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u'Прізвище є обов’язковим'
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u'Дата нородження є обов’язковою'
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u'Введіть корректний формат дати' \
                                         u'(напр. 1984-12-30)'
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u'Номер білета є обов’язковим'
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u'Оберіть групу для студента'
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u'Оберіть корректну групу'
                else:
                    data['student_group'] = Group.objects.get(pk=student_group)

            # Validate image field
            try:
                photo = Image.open(request.FILES.get('photo'))
            except IOError:
                errors['photo'] = u'Не вдалося відкрити файл'
                return render(request, 'students/students_add.html',
                    {'groups': groups,
                     'errors': errors})

            # Підстраховка
            if not Image.isImageType(photo):
                errors['photo'] = u'Файл не відповідає жодному типу зображення'
            elif request.FILES.get('photo').size > (1024**2) * 2:
                errors['photo'] = u'Зображення більше ніж 2 Мб'
            else:
                data['photo'] = request.FILES.get('photo')

            if not errors:
                 # Якщо дані були введені некоректно:
                 # Віддаємо форму разом із знайденими помилками
                # Якщо дані були введенні коректно:
                # Створюємо та зберігаємо студента в базу
                student = Student(**data)
                student.save()
                # Поретаємо користувача до списку студентів
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'students/students_add.html',
                    {'groups': groups,
                     'errors': errors})
        # Якщо кнопка Скасувати була натиснута:
        elif request.POST.get('cancel_button') is not None:
            # Повертаємо користувача до списку студентів
            return HttpResponseRedirect(reverse('home'))
    else:
        # Якщо форма не була запощена:
        # Поертаємо код початково стану форми
        return render(request, 'students/students_add.html', {'groups': groups})


def students_edit(request, id):
    return HttpResponse('<h1>Student %s edit</h1>' % id)


def students_delete(request, id):
    return HttpResponse('<h1>Student %s delete</h1>' % id)
