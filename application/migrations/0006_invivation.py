# Generated by Django 3.0.6 on 2020-08-11 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0005_auto_20200810_0432'),
    ]

    operations = [
        migrations.CreateModel(
            name='invivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('all_registrations', models.IntegerField(default=0)),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
