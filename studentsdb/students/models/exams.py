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

    pass
