# Generated by Django 4.1 on 2022-10-10 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_sublevel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='name',
        ),
    ]
