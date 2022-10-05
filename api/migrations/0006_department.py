# Generated by Django 4.1 on 2022-10-05 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_subject_classes_class_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.level')),
            ],
        ),
    ]
