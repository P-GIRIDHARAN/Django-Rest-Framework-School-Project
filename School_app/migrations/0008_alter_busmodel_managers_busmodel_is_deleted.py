# Generated by Django 5.1.6 on 2025-02-17 07:32

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('School_app', '0007_busmodel'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='busmodel',
            managers=[
                ('everything', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='busmodel',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
