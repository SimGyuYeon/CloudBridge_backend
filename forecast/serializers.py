from rest_framework import serializers

from .models import *


class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileList
        fields = "__all__"


class ModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelList
        fields = "__all__"


class PredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredList
        fields = "__all__"


class GraphListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphList
        fields = "__all__"
