# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20150616_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teampick',
            name='correct',
            field=models.BooleanField(default=False),
        ),
    ]
