from django.db import models


class CodeSnippet(models.Model):

    name = models.CharField(max_length=100)
    code = models.TextField()
    is_correct = models.BooleanField()

    owner = models.ForeignKey('auth.User', related_name='code_snippets', on_delete=models.CASCADE)

    def __repr__(self):
        return f"snippet with code - {self.code}"
