# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from contact_form.forms import ContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML
from crispy_forms.bootstrap import FormActions, StrictButton
from captcha.fields import CaptchaField

from ..models.students import Student
from ..models.groups import Group


class StudentCreateForm(forms.ModelForm):
    class Meta(object):
        model = Student
        fields = (
            'first_name', 'last_name', 'middle_name', 'birthday',
            'photo', 'student_group', 'ticket', 'notes',)
        widgets = {
            'birthday': forms.DateInput(),
            'notes': forms.Textarea(attrs={'cols': 10, 'rows': 4}),
        }

    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        super(StudentCreateForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # set layout
        self.helper.layout = Layout(
            Fieldset(
                u'Заповніть дані про студента',
                'first_name', 'last_name', 'middle_name', 'birthday',
                'photo', 'student_group', 'ticket', 'notes'
            ),
            # add buttons
            FormActions(
                Submit('add_button', u'Зберегти', css_class='btn-success'),
                HTML(u'<a class="btn btn-link" href="{% url "home" %}"'
                     u'role="button">Скасувати</a>')
            ),
        )

    def clean(self):
        cleaned_data = super(StudentCreateForm, self).clean()

        if cleaned_data.get('photo') is not None and cleaned_data.get('photo').size > (1024**2) * 2:
            msg = u'Файл зображення не повинен бути більше ніж 2 Мб'
            self.add_error('photo', msg)

        return cleaned_data


class StudentUpdateForm(StudentCreateForm):
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})

        self.helper.layout = Layout(
            Fieldset(
                u'Редагування студента {{ object }}',
                'first_name', 'last_name', 'middle_name', 'birthday',
                'photo', 'student_group', 'ticket', 'notes'
            ),
            # add buttons
            FormActions(
                Submit('add_button', u'Зберегти', css_class='btn-success'),
                StrictButton(u'Скасувати', name='cancel_button', type='submit',
                             css_class='btn-link')
            ),
        )


class GroupCreateForm(forms.ModelForm):
    class Meta(object):
        model = Group
        fields = ('title', 'leader', 'notes',)
        widgets = {'notes': forms.Textarea(attrs={'cols': 10, 'rows': 4})}

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # set layout
        self.helper.layout = Layout(
            Fieldset(
                u'Заповніть дані про групу',
                'title', 'leader', 'notes'
            ),
            # add buttons
            FormActions(
                Submit('add_button', u'Зберегти', css_class='btn-success'),
                HTML(u'<a class="btn btn-link" href="{% url "groups" %}"'
                     u'role="button">Скасувати</a>')
            ),
        )


class GroupEditForm(GroupCreateForm):
    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('groups_edit',
                                          kwargs={'pk': kwargs['instance'].id})

        self.helper.layout = Layout(
            Fieldset(
                u'Редагування групи {{ object }}',
                'title', 'leader', 'notes'
            ),
            # add buttons
            FormActions(
                Submit('add_button', u'Зберегти', css_class='btn-success'),
                StrictButton(u'Скасувати', name='cancel_button', type='submit',
                             css_class='btn-link')
            ),
        )


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
        self.helper.add_input(Submit('send_button', u'Надіслати',
                                     css_class='btn-success'))

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
