# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.groups import Group
from ..forms.forms import GroupCreateForm, GroupEditForm


# Views for groups
def groups_list(request):
    groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')

    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    paginator = Paginator(groups, 5)
    page = request.GET.get('page')

    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        groups = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html', {'groups': groups})


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
            return reverse('groups')
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
