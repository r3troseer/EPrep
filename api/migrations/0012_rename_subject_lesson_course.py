# Generated by Django 4.1 on 2022-10-08 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_delete_jss'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='subject',
            new_name='course',
        ),
    ]
