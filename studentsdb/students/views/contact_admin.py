# -*- coding: utf-8 -*-
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from contact_form.views import ContactFormView

from ..forms.forms import FeedbackForm


class FeedbackView(ContactFormView):
    form_class = FeedbackForm
    template_name = 'contact_admin/form.html'

    def get_success_url(self):
        return reverse('success_sending_email')


class SuccessRedirectView(RedirectView):
    pattern_name = 'contact_admin'

    def get_redirect_url(self, *args, **kwargs):
        HttpResponse('Redirecting...')
        return super(SuccessRedirectView, self).get_redirect_url(*args, **kwargs)
