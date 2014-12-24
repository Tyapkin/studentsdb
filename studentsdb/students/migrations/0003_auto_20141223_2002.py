# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20141222_2014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examresults',
            options={'verbose_name': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442', 'verbose_name_plural': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u0456\u0441\u043f\u0438\u0442\u0456\u0432'},
        ),
        migrations.AlterField(
            model_name='examresults',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0406\u0441\u043f\u0438\u0442', to='students.Exam', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examresults',
            name='grade',
            field=models.CharField(default=b'-1', max_length=2, verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430', choices=[(b'-1', b'No grade'), (b'0', b'F'), (b'1', b'E'), (b'2', b'D'), (b'3', b'C'), (b'4', b'B'), (b'5', b'A')]),
            preserve_default=True,
        ),
    ]
