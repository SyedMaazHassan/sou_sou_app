# Generated by Django 3.0.6 on 2020-08-16 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0022_auto_20200816_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift_record',
            name='POINTS',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gift_record',
            name='TIME',
            field=models.TimeField(default='11:28:43'),
        ),
        migrations.AlterField(
            model_name='sending_history',
            name='TIME',
            field=models.TimeField(default='11:28:43'),
        ),
    ]
