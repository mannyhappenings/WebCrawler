# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0003_page_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlDb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=128, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
