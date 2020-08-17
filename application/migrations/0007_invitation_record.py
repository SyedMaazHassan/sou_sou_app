# Generated by Django 3.0.6 on 2020-08-11 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0006_invivation'),
    ]

    operations = [
        migrations.CreateModel(
            name='invitation_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_provider', to=settings.AUTH_USER_MODEL)),
                ('registered_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
