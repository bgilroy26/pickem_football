# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='mascot',
            field=models.ImageField(upload_to='static/team', default='download.jpg'),
        ),
    ]
