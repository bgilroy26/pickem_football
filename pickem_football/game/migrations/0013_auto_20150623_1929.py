# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20150622_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='buy_in',
            field=models.DecimalField(max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='league',
            name='marquee',
            field=models.ImageField(blank=True, default='rose-bowl.jpg', upload_to='game/static/league'),
        ),
    ]
