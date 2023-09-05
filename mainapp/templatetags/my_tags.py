from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter
def image_path_filter(image):
    return os.path.join(settings.MEDIA_URL, str(image))

@register.simple_tag
def image_path_temp(image):
    return os.path.join(settings.MEDIA_URL, str(image))