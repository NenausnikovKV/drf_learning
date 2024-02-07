from rest_framework import serializers

from .models import CodeSnippet


class CodeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = CodeSnippet
        fields = "__all__"
