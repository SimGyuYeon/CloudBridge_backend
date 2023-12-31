# Generated by Django 4.0.6 on 2023-08-31 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file_path', models.FilePathField(path=None, recursive=True, verbose_name='파일 경로')),
                ('created_dt', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'FileList',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ModelList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_dt', models.DateTimeField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecast.filelist')),
            ],
            options={
                'db_table': 'ModelList',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PredList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pred_value', models.FloatField(verbose_name='예측값')),
                ('real_value', models.FloatField(verbose_name='실측값')),
                ('pred_dt', models.DateTimeField(verbose_name='예측 시간')),
                ('created_dt', models.DateTimeField()),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecast.modellist')),
            ],
            options={
                'db_table': 'PredList',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GraphList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path1', models.FilePathField(path=None, recursive=True, verbose_name='파일 경로1')),
                ('path2', models.FilePathField(path=None, recursive=True, verbose_name='파일 경로2')),
                ('path3', models.FilePathField(path=None, recursive=True, verbose_name='파일 경로3')),
                ('path4', models.FilePathField(path=None, recursive=True, verbose_name='파일 경로4')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecast.modellist')),
            ],
            options={
                'db_table': 'GraphList',
                'managed': True,
            },
        ),
    ]
