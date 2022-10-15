# Generated by Django 4.1 on 2022-10-12 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_lesson_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='body',
        ),
        migrations.AlterField(
            model_name='topic',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topic', to='api.lesson'),
        ),
    ]