# -*- coding: utf-8 -*-


def students_proc(request):
    from django.utils.encoding import smart_unicode
    # processor returns the root URL
    absolute_uri = smart_unicode(request.build_absolute_uri('/'))
    absolute_uri = absolute_uri[0:-1]
    return {'PORTAL_URL': absolute_uri}
