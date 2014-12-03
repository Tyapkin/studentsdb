# -*- coding: utf-8 -*-
from .settings import PORTAL_URL


def students_proc(request):
    # processor returns the root URL
    return {'PORTAL_URL': PORTAL_URL}
