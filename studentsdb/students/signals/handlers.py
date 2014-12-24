# -*- coding: utf-8 -*-
from django.dispatch import receiver
from .signals import create_exam_results

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
