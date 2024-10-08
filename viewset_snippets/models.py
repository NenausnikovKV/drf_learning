from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class ViewSetSnippet(models.Model):
    """
        Tutorial snippet.
    """
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()

    title = models.CharField(max_length=100, blank=True, default='')
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    owner = models.ForeignKey('auth.User', related_name='view_set_snippet', on_delete=models.CASCADE)
    highlighted = models.TextField(default="hello highlighted")

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    def __repr__(self):
        return f"snippet with code - {self.code}"


class ViewSetModelComment(models.Model):
    """
        Simple model for test serializer creating.
        It is used in testing.
    """
    email = models.CharField(max_length=30)
    content = models.CharField(max_length=30)
    created = models.DateTimeField()
