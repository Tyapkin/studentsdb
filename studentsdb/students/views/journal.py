# -*- coding: utf-8 -*-
from django.shortcuts import render


# Views for journal
def journal(request):
    return render(request, 'students/journal.html', {})
