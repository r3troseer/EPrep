# Generated by Django 4.1 on 2022-09-11 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.phonenumber'),
        ),
    ]
