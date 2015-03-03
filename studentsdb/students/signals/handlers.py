# -*- coding: utf-8 -*-
import logging
from django.dispatch import receiver
from .signals import create_exam_results, log_student_updated_added_event,\
    log_student_deleted_event

from ..models.exams import Exam, ExamResults
from ..models.students import Student


@receiver(create_exam_results, sender=Exam)
def create_exam_results_handler(sender, **kwargs):
    """
    Когда создаются экзамены для определенной группы, то этот обработчик,
    автоматически создает результаты экзаменов для всех студентов в группе.
    """

    exam_obj = kwargs.get('instance')
    results = ExamResults.objects.filter(exam=exam_obj)

    if not results:
        students = Student.objects.filter(
            student_group_id=exam_obj.exam_group.id)

        for student_result in students:
            result = ExamResults(exam=exam_obj, student=student_result)
            result.save()


@receiver(log_student_updated_added_event, sender=Student)
def log_student_updated_added_event_handler(sender, **kwargs):
    """
    Writes information about newly added or updated student into log file
    """
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    if kwargs['created']:
        logger.info('Student added: %s %s (ID: %d)', student.first_name,
                    student.last_name, student.id)
    else:
        logger.info('Student updated: %s %s (ID: %d)', student.first_name,
                    student.last_name, student.id)

@receiver(log_student_deleted_event, sender=Student)
def log_student_deleted_event_handler(sender, **kwargs):
    """
    Writes information about deleted student into log file
    """
    logger = logging.getLogger(__name__)

    student = kwargs.get('instance')
    logger.info('Student deleted: %s %s (ID: %d)', student.first_name,
                student.last_name, student.id)
