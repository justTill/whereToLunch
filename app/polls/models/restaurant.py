from django.db import models
from django.forms.widgets import Input


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100, unique=True)
    restaurant_color = ColorField(default='#ffffff')
    restaurant_menu_link = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.restaurant_name


class ColorWidget(Input):
    input_type = 'color'
    template_name = 'polls/forms/widgets/color.html'