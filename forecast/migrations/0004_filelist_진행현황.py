# Generated by Django 4.0.6 on 2023-09-06 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0003_alter_filelist_options_alter_graphlist_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filelist',
            name='진행현황',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
