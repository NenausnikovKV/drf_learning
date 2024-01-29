from rest_framework import serializers

from .models import Snippet


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ["id", "code", "title", "linenos", "language", "style"]
