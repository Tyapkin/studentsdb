from django.db import models
from django.utils.translation import ugettext_lazy as _


class Student(models.Model):
    """Student Model"""

    first_name = models.CharField(max_length=20, blank=False,
                                  verbose_name=_('First name'))

    last_name = models.CharField(max_length=20, blank=False,
                                 verbose_name=_('Last name'))

    middle_name = models.CharField(max_length=20, blank=True,
                                   verbose_name=_('Middle name'), default='')

    birthday = models.DateField(blank=False, verbose_name=_('Birthday'),
                                null=True)

    photo = models.ImageField(blank=True, verbose_name=_('Photo'), null=True)

    student_group = models.ForeignKey('Group', blank=False, null=True,
                                      on_delete=models.PROTECT,
                                      verbose_name=_('Group'))

    ticket = models.CharField(max_length=20, blank=False, unique=True,
                              verbose_name=_('Ticket'))

    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(object):
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
