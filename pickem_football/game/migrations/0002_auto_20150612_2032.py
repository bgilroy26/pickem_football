# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='losses',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='slug',
            field=models.SlugField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='wins',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(default=None, max_length=75, unique=True),
        ),
    ]
