# Generated by Django 3.0.6 on 2020-08-15 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0020_auto_20200812_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_parent_nodes',
            name='parent_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.tree_data'),
        ),
        migrations.AlterField(
            model_name='gift_record',
            name='DATE',
            field=models.DateField(default='2020-08-15'),
        ),
        migrations.AlterField(
            model_name='gift_record',
            name='TIME',
            field=models.TimeField(default='08:50:26'),
        ),
    ]
