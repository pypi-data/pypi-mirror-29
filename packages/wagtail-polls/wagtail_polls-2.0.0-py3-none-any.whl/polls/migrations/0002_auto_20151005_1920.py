# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={},
        ),
        migrations.RemoveField(
            model_name='poll',
            name='date',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='title',
        ),
        migrations.RemoveField(
            model_name='pollitem',
            name='image',
        ),
        migrations.RemoveField(
            model_name='pollitem',
            name='value',
        ),
        migrations.AddField(
            model_name='poll',
            name='message',
            field=wagtail.core.fields.RichTextField(help_text='Copy to show on the poll. For example a question.', blank=True),
        ),
        migrations.AddField(
            model_name='poll',
            name='name',
            field=models.CharField(default=datetime.datetime(2015, 10, 5, 19, 20, 13, 884186), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pollitem',
            name='message',
            field=wagtail.core.fields.RichTextField(verbose_name='Choice', blank=True),
        ),
    ]
