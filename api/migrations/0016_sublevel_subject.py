# Generated by Django 4.1 on 2022-10-10 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_class_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sublevel',
            name='subject',
            field=models.ManyToManyField(to='api.course'),
        ),
    ]
