# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Users', '0003_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('username', models.CharField(unique=True, max_length=20)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('fname', models.CharField(blank=True, max_length=20)),
                ('lname', models.CharField(blank=True, max_length=20)),
                ('userEmail', models.CharField(blank=True, max_length=45)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user_ptr',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
