# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20150208_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='fname',
            field=models.CharField(blank=True, verbose_name='First Name', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lname',
            field=models.CharField(blank=True, verbose_name='Last Name', max_length=20),
            preserve_default=True,
        ),
    ]
