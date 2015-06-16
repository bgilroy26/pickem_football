# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20150616_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='mascot',
            field=models.ImageField(blank=True, upload_to='game/static/team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(unique=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.SlugField(default=None, max_length=100),
        ),
    ]
