# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


# Views for students
def students_list(request):
    students = (
        {
            'id': 1,
            'first_name': u'Олександр',
            'last_name': u'Тяпкін',
            'ticket': u'030',
            'image': 'img/me.jpg'
        },
        {
            'id': 2,
            'first_name': u'Бендер',
            'last_name': u'Родрігес',
            'ticket': u'010',
            'image': 'img/Bender.jpg'
        },
        {
            'id': 3,
            'first_name': u'Філліп',
            'last_name': u'Фрай',
            'ticket': u'011',
            'image': 'img/Fry.jpg'
        }
    )
    return render(request, 'students/students_list.html',
                  {'students': students})


def students_add(request):
    return HttpResponse('<h1>Add form students</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Student %s edit</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Student %s delete</h1>' % sid)
