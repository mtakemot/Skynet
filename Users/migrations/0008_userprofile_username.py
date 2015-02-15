# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_remove_userprofile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=20, default=models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            preserve_default=True,
        ),
    ]
