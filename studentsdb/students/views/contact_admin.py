# -*- coding: utf-8 -*-
# from django import forms
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
# from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from contact_form.forms import ContactForm
from contact_form.views import ContactFormView
from captcha.fields import CaptchaField

# from studentsdb.settings import ADMIN_EMAIL


class FeedbackForm(ContactForm):
    # style for form
    def __init__(self, request=None, *args, **kwargs):
        # call original initializer
        super(FeedbackForm, self).__init__(request=request, *args, **kwargs)
        # this helper object allow us to customize form
        self.helper = FormHelper()
        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')
        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))

    subject_template_name = 'contact_admin/contact_form_subject.txt'

    template_name = 'contact_admin/contact_form.txt'

    def save(self, fail_silently=False):
        try:
            send_mail(fail_silently=fail_silently, **self.get_message_dict())
        except Exception:
            messages.error(self.request, u'Під час відправки листа сталася '
                                         u'непередбачувана помилка. Будь ласка, '
                                         u'спробуйте скористатися формою пізніше.')
        else:
            messages.success(self.request, u'Повідомлення було успішно надіслано.')

    captcha = CaptchaField()


"""
def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instanse and populate it with data from the request
        form = ContactForm(request.POST)

        # check whether user data is valid:
        if form.is_valid():
            # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                message = u'Під час відправки листа сталася' \
                          u'непередбачувана помилка.' \
                          u'Спробуйте скористатися даною формою пізніше.'
            else:
                message = u'Повідомлення успішно надіслано.'

            # redirect to same contact page with success message
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('contact_admin'), message))
    else:
        # if there was not POST render blank form
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})
"""


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

"""
Убрать django-contact-form. Создать полностью кастомную форму с помощью
FormView.
"""
