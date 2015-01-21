# -*- coding: utf-8 -*-
from datetime import datetime
from PIL import Image
from django.views.generic import UpdateView, DeleteView
from django.shortcuts import render
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

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
    # messages strings
    success_added_student = u'Студента %s %s успішно додано!'
    cancel_form = u'Додавання студента скасовано.'
    # Якщо форма була запощена:
    if request.method == 'POST':
        # Якщо кнопка Додати була натиснута:
        if request.POST.get('add_button') is not None:
            # Перевіряємо дані на коректність та збираємо помилки
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                messages.warning(request, u'Ім’я є обов’язковим', extra_tags='first_name')
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                messages.warning(request, u'Прізвище є обов’зковим', extra_tags='last_name')
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                messages.warning(request, u'Дата нородження є обов’язковою', extra_tags='birthday')
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    messages.warning(request, u'Введіть корректний формат дати'
                                              u'(напр. 1984-12-30)', extra_tags='birthday')
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                messages.warning(request, u'Номер білета є обов’язковим', extra_tags='ticket')
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                messages.warning(request, u'Оберіть групу для студента', extra_tags='student_group')
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    messages.warning(request, u'Оберіть корректну групу', extra_tags='student_group')
                else:
                    data['student_group'] = Group.objects.get(pk=student_group)

            # Validate image field
            if request.FILES.get('photo') is not None:
                try:
                    photo = Image.open(request.FILES.get('photo'))
                except IOError:
                    messages.warning(request, u'Не вдалося відкрити файл',
                                     extra_tags='photo')
                    return render(request, 'students/students_add.html',
                                  {'groups': groups})

                # Підстраховка
                if not Image.isImageType(photo):
                    messages.warning(request, u'Файл не відповідає жодному'
                                              u'типу зображення',
                                     extra_tags='photo')
                elif request.FILES.get('photo').size > (1024**2) * 2:
                    messages.warning(request, u'Зображення більше ніж 2 Мб',
                                     extra_tags='photo')
                else:
                    data['photo'] = request.FILES.get('photo')

            storage = messages.get_messages(request)

            if len(storage) == 0:
                # Якщо дані були введені некоректно:
                # Віддаємо форму разом із знайденими помилками
                # Якщо дані були введенні коректно:
                # Створюємо та зберігаємо студента в базу
                student = Student(**data)
                student.save()
                # Поретаємо користувача до списку студентів
                return HttpResponseRedirect(
                    reverse('home'), {'messages': messages.add_message(
                        request, messages.SUCCESS, success_added_student % (first_name, last_name))})
            else:
                return render(request, 'students/students_add.html',
                              {'groups': groups})
        # Якщо кнопка Скасувати була натиснута:
        elif request.POST.get('cancel_button') is not None:
            # Повертаємо користувача до списку студентів
            return HttpResponseRedirect(
                reverse('home'), {'messages': messages.add_message(
                    request, messages.INFO, cancel_form)})
    else:
        # Якщо форма не була запощена:
        # Поертаємо код початково стану форми
        return render(request, 'students/students_add.html', {'groups': groups})


class StudentUpdateForm(ModelForm):
    class Meta(object):
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class='btn btn-primary'),
            Submit('cancel_button', u'Скасувати', css_class='btn btn-link'),
        )


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/student_edit.html'
    form_class = StudentUpdateForm
    success_msg = u'Студента успішно збережено'
    cancel_msg = u'Редагування студента скасовано'

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), self.success_msg,)

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('home'), self.cancel_msg)
            )
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'
    success_msg = u'Студента успішно видалено.'

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), self.success_msg)
