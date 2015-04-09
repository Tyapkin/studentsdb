from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from ..util import paginate, get_current_group
from ..models.students import Student
from ..forms.forms import StudentCreateForm, StudentUpdateForm


# Class based views for students
class StudentListView(ListView):
    template_name = 'students/students_list.html'
    model = Student

    def get_queryset(self):
        # check if we need to show only one group of students
        current_group = get_current_group(self.request)

        if current_group:
            # get queryset from Student for one group
            object_list = Student.objects.filter(student_group=current_group)
        else:
            # otherwise show all students
            object_list = Student.objects.all()

        return object_list

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)

        # get variable 'order_by' from request.GET
        order_by = self.request.GET.get('order_by', '')

        # try to order students list
        if order_by in ('last_name', 'first_name', 'ticket'):
            self.object_list = self.object_list.order_by(order_by)

            # if reverse in request.GET
            if self.request.GET.get('reverse', '') == '1':
                # sort student list reverse
                self.object_list = self.object_list.reverse()
        else:
            self.object_list = self.object_list.order_by('last_name')

        context = paginate(self.object_list, 5, self.request, context,
                           var_name='students')

        return context


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = 'students/students_form.html'
    success_msg = _('Student successfully added')
    cancel_msg = _('Adding student canceled')

    def get_form_kwargs(self):
        kwargs = super(StudentCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            messages.warning(self.request, self.cancel_msg)
            return reverse('home')
        else:
            return super(StudentCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('home')


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_form.html'
    form_class = StudentUpdateForm
    success_msg = _('The student successfully saved')
    cancel_msg = _('Saving the student canceled')

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            messages.warning(self.request, self.cancel_msg)
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'
    success_msg = _('The student successfully removed')

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('home')


class LanguageSelect(View):

    def get(self, request, code, *args, **kwargs):
        next = request.META.get('HTTP_REFERER', '/')
        response = HttpResponseRedirect(next)
        if code and translation.check_for_language(code):
            if hasattr(request, 'session'):
                request.session['django_language'] = code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, code)
            translation.activate(code)
        return response
