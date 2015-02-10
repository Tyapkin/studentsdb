# -*- coding: utf-8 -*-


def students_proc(request):
    from django.utils.encoding import smart_unicode
    # processor returns the root URL
    absolute_uri = smart_unicode(request.build_absolute_uri('/'))
    absolute_uri = absolute_uri[0:-1]

    adding = None
    editing = None

    if '/students/' in request.path and '/add/' in request.path or \
       '/edit/' in request.path:
        adding = u'Додати студента'
        editing = u'Редагування студента'
    elif '/groups/' in request.path and '/add/' in request.path or \
         '/edit/' in request.path:
        adding = u'Додати групу'
        editing = u'Редагування групи'
    elif '/exams/' in request.path and '/add/' in request.path or \
         '/edit/' in request.path:
        adding = u'Додати екзамен'
        editing = u'Редагування екзамену'

    return {
        'PORTAL_URL': absolute_uri,
        'ADDING': adding,
        'EDITING': editing
    }
