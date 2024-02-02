from rest_framework import serializers

from .models import CodeSnippet


class CodeSerializer(serializers.ModelSerializer):
    #  todo move to new app
    class Meta:
        model = CodeSnippet
        fields = "__all__"
