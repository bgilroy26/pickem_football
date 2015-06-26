# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_teampick_game_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teampick',
            name='choice',
            field=models.CharField(default=None, max_length=70),
        ),
    ]
