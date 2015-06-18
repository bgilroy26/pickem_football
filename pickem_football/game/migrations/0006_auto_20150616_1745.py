# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20150616_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='mascot',
            field=models.ImageField(upload_to='game/static/team', blank=True, default=None),
        ),
    ]
