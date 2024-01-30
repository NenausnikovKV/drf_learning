from django.db import models


class CodeSnippet(models.Model):
    """
        Rudimentary model. Minimal model field and methods for drf.
    """
    name = models.CharField(max_length=100)
    code = models.TextField()
    is_Correct = models.BooleanField()

    def __repr__(self):
        return f"snippet with code - {self.code}"
