# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('students', '0004_auto_20150217_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('degree', models.CharField(max_length=50, verbose_name='degree', blank=True)),
                ('middle_name', models.CharField(max_length=30, verbose_name='patronymic', blank=True)),
                ('phone_num', models.CharField(help_text='Enter a phone number. Example: 0675554433 or +380675554433', max_length=13, verbose_name='phone number', blank=True)),
                ('address', models.TextField(verbose_name='address', blank=True)),
                ('photo', models.ImageField(upload_to=b'', null=True, verbose_name='your photo', blank=True)),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teachers',
            },
            bases=('auth.user',),
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': 'An exam', 'verbose_name_plural': 'Examinations'},
        ),
        migrations.AlterModelOptions(
            name='examresults',
            options={'verbose_name': 'Result', 'verbose_name_plural': 'Exam results'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
        migrations.AlterModelOptions(
            name='monthjournal',
            options={'verbose_name': 'Monthly journal', 'verbose_name_plural': 'Monthly journals'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AlterField(
            model_name='exam',
            name='auditorium',
            field=models.CharField(default=b'a1', max_length=2, verbose_name='Auditorium', choices=[(b'a1', b'101'), (b'a2', b'102'), (b'a3', b'103'), (b'a4', b'201'), (b'a5', b'202'), (b'a6', b'203')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exam',
            name='date_exam',
            field=models.DateTimeField(verbose_name='The date of the exam'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Group', blank=True, to='students.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_name',
            field=models.CharField(max_length=40, verbose_name='Exam title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exam',
            name='teacher',
            field=models.CharField(max_length=40, verbose_name='Teacher'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examresults',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='An exam', to='students.Exam', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examresults',
            name='grade',
            field=models.CharField(default=b'-1', max_length=2, verbose_name='Grade', choices=[(b'-1', 'No grade'), (b'0', b'F'), (b'1', b'E'), (b'2', b'D'), (b'3', b'C'), (b'4', b'B'), (b'5', b'A')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examresults',
            name='student',
            field=models.ForeignKey(verbose_name='Student', blank=True, to='students.Student', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student', verbose_name='Leader'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='notes',
            field=models.TextField(verbose_name='Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=20, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='date',
            field=models.DateField(verbose_name='Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='student',
            field=models.ForeignKey(unique_for_month=b'date', verbose_name='Student', to='students.Student'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Birthday'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=20, verbose_name='First name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=20, verbose_name='Last name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default=b'', max_length=20, verbose_name='Middle name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(verbose_name='Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Group', to='students.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.CharField(unique=True, max_length=20, verbose_name='Ticket'),
            preserve_default=True,
        ),
    ]
