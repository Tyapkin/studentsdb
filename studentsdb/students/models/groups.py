from django.db import models
from django.utils.translation import ugettext_lazy as _


class Group(models.Model):
    """Model Group"""

    title = models.CharField(max_length=20, blank=False,
                             verbose_name=_('Title'))

    leader = models.OneToOneField('Student', blank=True, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=_('Leader'))

    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(object):
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __unicode__(self):
        if self.leader:
            return '%s (%s %s)' % (self.title, self.leader.first_name,
                                   self.leader.last_name)
        else:
            return '%s' % self.title
