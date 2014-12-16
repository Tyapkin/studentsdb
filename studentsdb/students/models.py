# -*- coding: utf-8 -*-
from django.db import models


class Student(models.Model):
    """Student Model"""

    first_name = models.CharField(
        max_length=20,
        blank=False,
        verbose_name=u'Ім’я')
    last_name = models.CharField(
        max_length=20,
        blank=False,
        verbose_name=u'Прізвище')
    middle_name = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=u'По-батькові',
        default='')
    birthday = models.DateField(
        blank=False,
        verbose_name=u'Дата народження',
        null=True)
    photo = models.ImageField(
        blank=True,
        verbose_name=u'Фото',
        null=True)
    student_group = models.ForeignKey(
        'Group',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=u'Група')
    ticket = models.CharField(
        max_length=20,
        blank=False,
        verbose_name=u'Білет')
    notes = models.TextField(
        blank=True,
        verbose_name=u'Додаткові нотатки')

    class Meta(object):
        verbose_name = u'Студент'
        verbose_name_plural = u'Студенти'

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Group(models.Model):
    """Model Group"""

    title = models.CharField(
        max_length=20,
        blank=False,
        verbose_name=u'Назва')
    leader = models.OneToOneField(
        'Student',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=u'Староста')
    notes = models.TextField(
        blank=True,
        verbose_name=u'Додаткові нотатки')

    class Meta(object):
        verbose_name = u'Група'
        verbose_name_plural = u'Групи'

    def __unicode__(self):
        if self.leader:
            return '%s (%s %s)' % (self.title, self.leader.first_name,
                                   self.leader.last_name)
        else:
            return '%s' % self.title
