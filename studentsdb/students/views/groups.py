# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..models.groups import Group
from ..forms.forms import GroupCreateForm, GroupEditForm
from ..util import paginate


# Class based views for groups
class GroupListView(ListView):
    template_name = 'students/groups_list.html'
    model = Group

    def get_queryset(self):
        object_list = Group.objects.all()

        # try to order groups list
        order_by = self.request.GET.get('order_by', '')

        if order_by in ('title', 'leader'):
            object_list = object_list.order_by(order_by)

            if self.request.GET.get('reverse', '') == '1':
                object_list = object_list.reverse()
        else:
            object_list = object_list.order_by('title')

        return object_list

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)

        context = paginate(self.object_list, 5, self.request, context,
                           var_name='group_list')

        return context


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'students/groups_form.html'
    success_msg = u'Групу успішно додано.'

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return reverse('groups')
        else:
            return super(GroupCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('groups')


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupEditForm
    template_name = 'students/groups_form.html'
    success_msg = u'Групу успішно збережено.'
    cancel_msg = u'Редагування групи скасовано.'

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            messages.warning(self.request, self.cancel_msg)
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('groups')


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/group_confirm_delete.html'
    success_msg = u'Групу успішно видалено.'

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('groups')
