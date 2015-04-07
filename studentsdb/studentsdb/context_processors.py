from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode


def students_proc(request):
    # processor returns the root URL
    absolute_uri = smart_unicode(request.build_absolute_uri('/'))
    absolute_uri = absolute_uri[0:-1]

    adding = None
    editing = None

    if '/students/' in request.path and '/add/' in request.path or '/students/'\
            in request.path and '/edit/' in request.path:
        adding = _('Add student')
        editing = _('Editing student')
        print 'returned students ==>> ', request.path
    elif '/groups/' in request.path and '/add/' in request.path or '/groups/'\
            in request.path and '/edit/' in request.path:
        adding = _('Add a group')
        editing = _('Editing group')
        print 'returned groups ==>> ', request.path
    elif '/exams/' in request.path and '/add/' in request.path or '/exams/'\
            in request.path and '/edit/' in request.path:
        adding = _('Add an exam')
        editing = _('Editing exam')
        print 'returned exams ==>> ', request.path

    return {
        'PORTAL_URL': absolute_uri,
        'ADDING': adding,
        'EDITING': editing
    }

# TODO: to deal with the localization of the processor
