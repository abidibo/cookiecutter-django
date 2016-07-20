from django import template

from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode

register = template.Library()

def sorl_thumbnail(parser, token):
    return ThumbnailNode(parser, token)

register.tag(sorl_thumbnail)
