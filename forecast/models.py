from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


def upload_to_today(instance, filename):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"uploads/{today}/{filename}"


# 바꿔도 됨
# file_path = models.FilePathField(
#     ("파일 경로"), path=None, match=None, recursive=True, max_length=100
# )
class FileList(models.Model):
    name = models.CharField(max_length=50)
    파일 = models.FileField(upload_to=upload_to_today, null=True)
    진행현황 = models.CharField(max_length=50, null=True)
    created_dt = models.DateTimeField(auto_now=True, auto_now_add=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "FileList"
        # managed = True


class ModelList(models.Model):
    name = models.CharField(max_length=50)
    created_dt = models.DateTimeField(auto_now=False, auto_now_add=False)

    file = models.ForeignKey(FileList, on_delete=models.CASCADE)

    class Meta:
        db_table = "ModelList"
        # managed = True


class PredList(models.Model):
    pred_value = models.FloatField(("예측값"))
    real_value = models.FloatField(("실측값"))
    pred_dt = models.DateTimeField(("예측 시간"), auto_now=False, auto_now_add=False)
    created_dt = models.DateTimeField(auto_now=False, auto_now_add=False)

    model = models.ForeignKey(ModelList, on_delete=models.CASCADE)

    class Meta:
        db_table = "PredList"
        # managed = True


class GraphList(models.Model):
    # 바꿔도 됨
    path1 = models.FilePathField(
        ("파일 경로1"), path=None, match=None, recursive=True, max_length=100
    )
    path2 = models.FilePathField(
        ("파일 경로2"), path=None, match=None, recursive=True, max_length=100
    )
    path3 = models.FilePathField(
        ("파일 경로3"), path=None, match=None, recursive=True, max_length=100
    )
    path4 = models.FilePathField(
        ("파일 경로4"), path=None, match=None, recursive=True, max_length=100
    )

    model = models.ForeignKey(ModelList, on_delete=models.CASCADE)

    class Meta:
        db_table = "GraphList"
        # managed = True
