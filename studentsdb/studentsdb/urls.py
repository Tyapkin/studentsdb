from .settings import MEDIA_ROOT, DEBUG
from django.conf.urls import patterns, include, url
from django.contrib import admin

from students.views.contact_admin import FeedbackView, SuccessRedirectView
from students.views.students import StudentCreateView, StudentUpdateView,\
    StudentDeleteView, StudentListView
from students.views.groups import GroupCreateView, GroupDeleteView, \
    GroupUpdateView, GroupListView
from students.views.exams import ExamCreateView, ExamEditView, ExamDeleteView, \
    ExamListView
from students.views.journal import JournalView

urlpatterns = patterns(
    '',
    # URL pattern for students
    url(r'^$', StudentListView.as_view(), name='home'),
    url(r'^students/add/$', StudentCreateView.as_view(), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$',
        StudentDeleteView.as_view(), name='students_delete'),
    # URL pattern for groups
    url(r'^groups/$', GroupListView.as_view(), name='groups'),
    url(r'^groups/add/$',
        GroupCreateView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(),
        name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$',
        GroupDeleteView.as_view(), name='groups_delete'),
    # URL pattern for journal
    url(r'^journal/$', JournalView.as_view(), name='journal'),
    # URL pattern for exam
    url(r'^exams/$', ExamListView.as_view(), name='exams'),
    url(r'^exams/add/$', ExamCreateView.as_view(), name='add_exam'),
    url(r'^exams/(?P<pk>\d+)/delete/$',
        ExamDeleteView.as_view(), name='delete_exam'),
    url(r'^exams/(?P<pk>\d+)/edit/$',
        ExamEditView.as_view(), name='edit_exam'),
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
