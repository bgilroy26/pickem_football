# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20150618_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='marquee',
            field=models.ImageField(upload_to='game/static/league', default='rose-bowl.jpg'),
        ),
        migrations.AlterField(
            model_name='league',
            name='nfl_year',
            field=models.IntegerField(default=2014),
        ),
        migrations.AlterField(
            model_name='team',
            name='mascot',
            field=models.ImageField(upload_to='game/static/team', default='download.jpg'),
        ),
    ]
