# -*- coding: utf-8 -*-
from django.db import models


class Group(models.Model):
    """Model Group"""

    title = models.CharField(max_length=20, blank=False,
                             verbose_name=u'Назва')

    leader = models.OneToOneField('Student', blank=True, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u'Староста')

    notes = models.TextField(blank=True, verbose_name=u'Додаткові нотатки')

    class Meta(object):
        verbose_name = u'Група'
        verbose_name_plural = u'Групи'

    def __unicode__(self):
        if self.leader:
            return '%s (%s %s)' % (self.title, self.leader.first_name,
                                   self.leader.last_name)
        else:
            return '%s' % self.title
