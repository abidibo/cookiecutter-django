from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import PageForm
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
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
    list_display = ('url', 'title', 'published', )
    list_filter = ('sites', 'registration_required', 'published', )
    search_fields = ('url', 'title')
