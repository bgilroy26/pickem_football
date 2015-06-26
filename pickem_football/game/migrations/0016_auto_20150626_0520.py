# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_auto_20150626_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teampick',
            name='choice',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]
