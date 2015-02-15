# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Packages', '0001_initial'),
        ('Users', '0005_auto_20150208_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='services',
            field=models.ManyToManyField(to='Packages.Service'),
            preserve_default=True,
        ),
    ]
