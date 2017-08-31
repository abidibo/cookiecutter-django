from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import PageForm
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm

    {% if cookiecutter.admin == 'django-baton' %}
    fieldsets = (
        (_('Main'), {
            'fields': ('url', 'title', 'content', 'tags', 'sites',
                       'enable_social_sharing', 'published', ),
            'classes': ('baton-tabs-init', 'baton-tab-fs-seo',
                        'baton-tab-fs-adv')
        }),
        (_('SEO'), {
            'classes': ('tab-fs-seo',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', ),
        }),
        (_('Advanced options'), {
            'classes': ('tab-fs-adv',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
    {% else %}
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'tags', 'sites',
                           'enable_social_sharing', 'published', )}),
        (_('SEO'), {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', ),
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
    {% endif %}
    list_display = ('url', 'title', 'published', )
    list_filter = ('sites', 'registration_required', 'published', )
    search_fields = ('url', 'title')
