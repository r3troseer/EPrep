# Generated by Django 4.1 on 2022-10-08 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_subject_course_rename_topic_lesson'),
    ]

    operations = [
        migrations.DeleteModel(
            name='jss',
        ),
    ]