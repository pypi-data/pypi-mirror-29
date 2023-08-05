from django.db import models
from cms.models import CMSPlugin
from pygments.styles import get_all_styles
from pygments.lexers import get_all_lexers

STYLE_CHOICES = map(lambda x: (x,x), get_all_styles())

LANGUAGE_CHOICES = list(map(lambda x: (x[1][0], x[0]), get_all_lexers()))
LANGUAGE_CHOICES.sort(key=lambda x: x[0])

class PygmentsPlugin(CMSPlugin):
    # It's a bad idea to set language/style choices here
    # What happens if styles/lexers change in pygments?
    # see: https://github.com/jedie/cmsplugin-pygments/issues/3
    code_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    style = models.CharField(max_length=255, choices=STYLE_CHOICES)
    linenumbers = models.BooleanField(default=True)


