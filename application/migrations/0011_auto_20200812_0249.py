# Generated by Django 3.0.6 on 2020-08-12 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20200812_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift_record',
            name='TIME',
            field=models.TimeField(default='02:49:55'),
        ),
    ]
