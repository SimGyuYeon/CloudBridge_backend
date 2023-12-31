# Generated by Django 4.0.6 on 2023-09-12 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0005_alter_modellist_created_dt_alter_predlist_created_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='predlist',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forecast.filelist'),
        ),
        migrations.AlterField(
            model_name='predlist',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forecast.modellist'),
        ),
    ]
