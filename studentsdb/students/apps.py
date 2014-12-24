# -*- coding: utf-8 -*-
from django.apps import AppConfig


class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = 'Students Application'

    def ready(self):
        # Импорт обработчиков сигналов
        import students.signals.handlers
