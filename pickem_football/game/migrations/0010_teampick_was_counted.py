# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20150616_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='teampick',
            name='was_counted',
            field=models.BooleanField(default=False),
        ),
    ]
