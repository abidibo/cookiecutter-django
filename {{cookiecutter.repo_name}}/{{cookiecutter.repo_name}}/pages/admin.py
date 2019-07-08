from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import PageForm
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm

    
    fieldsets = (
        (_('Main'), {
            'fields': ('url', 'title', 'content', 'tags', 'sites',
                       'enable_social_sharing', 'status', ),
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
    
    list_display = ('url', 'title', 'status', )
    list_editable = ('status', )
    list_filter = ('sites', 'registration_required', 'status', )
    search_fields = ('url', 'title')
