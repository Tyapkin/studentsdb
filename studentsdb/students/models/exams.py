# -*- coding: utf-8 -*-
from django.db import models


class Exam(models.Model):
    """Exams model"""

    AUDITORIUM_LIST = (
        ('a1', '101'), ('a2', '102'), ('a3', '103'),
        ('a4', '201'), ('a5', '202'), ('a6', '203'),
    )

    exam_name = models.CharField(max_length=40, blank=False,
                                 verbose_name=u'Назва іспиту')

    date_exam = models.DateTimeField(blank=False,
                                     verbose_name=u'Дата проведення іспиту')

    teacher = models.CharField(max_length=40, blank=False,
                               verbose_name=u'Викладач')

    exam_group = models.ForeignKey('Group', blank=True, null=True,
                                   on_delete=models.SET_NULL,
                                   verbose_name=u'Група')

    auditorium = models.CharField(max_length=2, choices=AUDITORIUM_LIST,
                                  default=u'a1',
                                  verbose_name=u'Аудиторія')

    class Meta(object):
        verbose_name = u'Іспит'
        verbose_name_plural = u'Іспити'

    def __unicode__(self):
        if self.teacher:
            return '%s (%s)' % (self.exam_name, self.teacher)
        else:
            return '%s' % self.exam_name


class ExamResults(models.Model):
    """Exam results model"""

    GRADE_LIST = (
        # Grades 'A, B, C, D, E, F' and default value 'No grade'
        ('-1', 'No grade'), ('0', 'F'), ('1', 'E'),
        ('2', 'D'), ('3', 'C'), ('4', 'B'), ('5', 'A'),
    )

    exam = models.ForeignKey('Exam', blank=False, null=True,
                             on_delete=models.PROTECT, verbose_name=u'Іспит')

    student = models.ForeignKey('Student', blank=True, null=True,
                                verbose_name=u'Студент')

    grade = models.CharField(max_length=2, choices=GRADE_LIST,
                             default='-1',
                             verbose_name=u'Оцінка')

    class Meta(object):
        verbose_name = u'Результат'
        verbose_name_plural = u'Результати іспитів'
        unique_together = ('exam', 'student')

    def __unicode__(self):

        if self.exam.exam_name and self.student:
            return '%s - %s' % (self.exam.exam_name, self.student)
        else:
            return 'Not found exam or student'
