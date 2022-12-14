# Generated by Django 4.1 on 2022-10-30 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_rename_name_topic_note'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0005_plan_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paystack_charge_id', models.CharField(blank=True, default='', max_length=100)),
                ('paystack_access_code', models.CharField(blank=True, default='', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('paid', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('payment_for', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.sublevel')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
