# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, post_delete

create_exam_results = post_save
log_student_updated_added_event = post_save
log_student_deleted_event = post_delete
