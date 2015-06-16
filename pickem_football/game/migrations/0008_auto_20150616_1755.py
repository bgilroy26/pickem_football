# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20150616_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.SlugField(),
        ),
    ]
