# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20150616_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='team',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
