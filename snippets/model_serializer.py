from rest_framework import serializers

from .models import Snippet


class ModelSerializer(serializers.ModelSerializer):
    #  todo move to new app
    class Meta:
        model = Snippet
        fields = ["id", "code", "title", "linenos", "language", "style"]
