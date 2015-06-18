from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Teacher(User):
    degree = models.CharField(_('degree'), max_length=50, blank=True)
    middle_name = models.CharField(_('patronymic'), max_length=30, blank=True)
    phone_num = models.CharField(_('phone number'), max_length=13, blank=True,
                                 help_text=_('Enter a phone number. Example: 0675554433 or +380675554433'))
    address = models.TextField(_('address'), blank=True)
    photo = models.ImageField(_('your photo'), blank=True, null=True)

    class Meta(object):
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    def __unicode__(self):
        return '%s' % self.username

    def get_full_name(self):
        # returns full name with middle_name if filled
        if self.middle_name:
            full_name = '%s %s %s' % (self.last_name, self.first_name, self.middle_name)
        else:
            full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()
