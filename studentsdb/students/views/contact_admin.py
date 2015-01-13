# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from studentsdb.settings import ADMIN_EMAIL


class ContactForm(forms.Form):
    from_email = forms.EmailField(label=u'Ваша е-майл адреса')
    subject = forms.CharField(label=u'Заголовок повідомлення',
                              max_length=128)
    message = forms.CharField(label=u'Текст повідомлення',
                              max_length=2560,
                              widget=forms.Textarea)


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
