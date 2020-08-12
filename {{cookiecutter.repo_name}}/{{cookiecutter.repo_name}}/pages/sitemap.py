from django.contrib.sitemaps import Sitemap
from .models import Page


class PageSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Page.objects.published()

    def changefreq(self, obj):
        return "weekly"
