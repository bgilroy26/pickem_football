# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20150612_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='pic',
        ),
        migrations.AddField(
            model_name='league',
            name='marquee',
            field=models.ImageField(blank=True, upload_to='game/static/league'),
        ),
        migrations.AddField(
            model_name='team',
            name='champion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='mascot',
            field=models.ImageField(blank=True, upload_to='game/static/team'),
        ),
    ]
