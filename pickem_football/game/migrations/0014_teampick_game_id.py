# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20150623_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='teampick',
            name='game_id',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
