from rest_framework import serializers

from json_snippets.models import CodeSnippet


class CodeSnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    is_correct = serializers.BooleanField()

    def create(self, validated_data):
        """
            Create and return a new `Snippet` instance, given the validated data.
        """
        return CodeSnippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
            Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.is_correct = validated_data.get('is_correct', instance.is_correct)
        instance.save()
        return instance
