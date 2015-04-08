from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _


def students_proc(request):
    # processor returns the root URL
    absolute_uri = smart_unicode(request.build_absolute_uri('/'))
    absolute_uri = absolute_uri[0:-1]

    adding = None
    editing = None
    trans_strings = (
        (_('Add student'), _('Editing student'),),
        (_('Add a group'), _('Editing group'),),
        (_('Add an exam'), _('Editing exam'),),
    )

    if '/students/' in request.path and '/add/' in request.path or '/students/'\
            in request.path and '/edit/' in request.path:
        adding = trans_strings[0][0]
        editing = trans_strings[0][1]
    elif '/groups/' in request.path and '/add/' in request.path or '/groups/'\
            in request.path and '/edit/' in request.path:
        adding = trans_strings[1][0]
        editing = trans_strings[1][1]
    elif '/exams/' in request.path and '/add/' in request.path or '/exams/'\
            in request.path and '/edit/' in request.path:
        adding = trans_strings[2][0]
        editing = trans_strings[2][1]

    return {
        'PORTAL_URL': absolute_uri,
        'ADDING': adding,
        'EDITING': editing
    }

# TODO: to deal with the localization of the processor
