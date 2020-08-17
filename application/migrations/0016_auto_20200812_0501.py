# Generated by Django 3.0.6 on 2020-08-12 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_auto_20200812_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='tree_data',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='node_parent', to='application.tree_data'),
        ),
        migrations.AlterField(
            model_name='gift_record',
            name='TIME',
            field=models.TimeField(default='05:01:54'),
        ),
    ]
