from rest_framework import serializers

from .models import *


class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileList
        fields = "__all__"
