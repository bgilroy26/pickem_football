# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20150626_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='marquee',
            field=models.ImageField(blank=True, default='rose-bowl.jpg', upload_to='static/league'),
        ),
        migrations.AlterField(
            model_name='league',
            name='nfl_year',
            field=models.IntegerField(default=2015),
        ),
        migrations.AlterField(
            model_name='team',
            name='mascot',
            field=models.ImageField(default='download.jpg', upload_to='static/team'),
        ),
    ]
