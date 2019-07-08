from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.sites.models import Site
from django.db import models
from django.urls import get_script_prefix
from django.utils.encoding import iri_to_uri, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager


@python_2_unicode_compatible
class Page(models.Model):
    DRAFT = 1
    PUBLISHED = 2
    ARCHIVED = 3

    STATUS_CHOICES = (
        (DRAFT, 'bozza'),
        (PUBLISHED, 'pubblicato'),
        (ARCHIVED, 'archiviato'),
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_('parent'),
        on_delete=models.SET_NULL,
        related_name='children',
        blank=True,
        null=True,
        help_text=_('Used to compose breadcrumbs'))
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = RichTextUploadingField(verbose_name=_('content'), blank=True)
    tags = TaggableManager(
        _('tags'), help_text=_('comma separated values'), blank=True)
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            "Example: 'pages/contact_page.html'. If this isn't provided, "
            "the system will use 'pages/default.html'."),
    )
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=
        _("If this is checked, only logged-in users will be able to view the page."
          ),  # noqa
        default=False,
    )
    enable_social_sharing = models.BooleanField(
        _('enable social sharing'), default=False)
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    # seo
    meta_title = models.CharField(
        _('meta title'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_('default to page title'))
    meta_description = models.TextField(
        _('meta description'),
        blank=True,
        null=True,
        help_text=_('default to first 20 words of content'))
    meta_keywords = models.CharField(
        _('meta keywords'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_('default to page tags'))

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ('url', )

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
