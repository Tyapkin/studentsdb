from .settings import MEDIA_ROOT, DEBUG
from django.conf.urls import patterns, include, url
from django.contrib import admin

from students.views.contact_admin import FeedbackView, SuccessRedirectView
from students.views.students import StudentUpdateView, StudentDeleteView

urlpatterns = patterns(
    '',
    # URL pattern for students
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$', 'students.views.students.students_add',
        name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$',
        StudentDeleteView.as_view(), name='students_delete'),
    # URL pattern for groups
    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/add/$',
        'students.views.groups.groups_add', name='groups_add'),
    url(r'^groups/(?P<id>\d+)/edit/$', 'students.views.groups.groups_edit',
        name='groups_edit'),
    url(r'^groups/(?P<id>\d+)/delete/$',
        'students.views.groups.groups_delete', name='groups_delete'),
    # URL pattern for journal
    url(r'^journal/$', 'students.views.journal.journal', name='journal'),
    # URL pattern for exam
    url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
    url(r'^exams/add/$', 'students.views.exams.add_exam', name='add_exam'),
    url(r'^exams/(?P<id>\d+)/delete/$',
        'students.views.exams.delete_exam', name='delete_exam'),
    url(r'^exams/(?P<id>\d+)/edit/$',
        'students.views.exams.edit_exam', name='edit_exam'),
    url(r'^exams/(?P<id>\d+)/results/$',
        'students.views.exams.exam_results', name='exam_results'),
    url(r'^exams/(?P<id>\d+)/result/delete/$',
        'students.views.exams.delete_exam_result', name='delete_exam_result'),
    url(r'^exams/(?P<id>\d+)/result/edit/$',
        'students.views.exams.edit_exam_result', name='edit_exam_result'),
    # admin contact form
    url(r'^contact_admin/$', FeedbackView.as_view(), name='contact_admin'),
    url(r'^success_sending_email/$', SuccessRedirectView.as_view(),
        name='success_sending_email'),
    # simple captcha
    url(r'^captcha/', include('captcha.urls')),
    # admin url
    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve', {
                'document_root': MEDIA_ROOT}),
    )
