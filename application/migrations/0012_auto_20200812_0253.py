# Generated by Django 3.0.6 on 2020-08-12 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_auto_20200812_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='is_paid',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='points',
            field=models.FloatField(default=500.0),
        ),
        migrations.AlterField(
            model_name='gift_record',
            name='TIME',
            field=models.TimeField(default='02:53:01'),
        ),
    ]
