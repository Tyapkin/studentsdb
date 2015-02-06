# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.groups import Group


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


def groups_add(request):
    return HttpResponse('<h1>Add group</h1>')


def groups_edit(request, pk):
    return HttpResponse('<h1>Edit group %s</h1>' % pk)


def groups_delete(request, pk):
    return HttpResponse('<h1>Delete group %s</h2>' % pk)

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/group_confirm_delete.html'
    success_msg = u'Групу успішно видалено.'

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('home')
