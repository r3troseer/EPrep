# Generated by Django 4.1 on 2022-10-26 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_userplan_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='duration',
            field=models.PositiveIntegerField(default=7),
        ),
    ]
