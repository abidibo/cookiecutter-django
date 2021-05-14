from django.conf.urls import include, url
from django.urls import path, re_path
{% if cookiecutter.use_django_baton == 'y' %}
from baton.autodiscover import admin
{% else %}
from django.contrib import admin
{% endif %}
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.views.generic import TemplateView
from django.views import static
from django.contrib.staticfiles.views import serve

from pages.sitemap import PageSitemap

sitemaps = {
    'pages': PageSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),

    {% if cookiecutter.use_django_baton == 'y' %}
    path('baton/', include('baton.urls')),
    {% endif %}

    re_path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt'), name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    {% if cookiecutter.use_filer == 'y' %}
    path('filer/', include('filer.urls')),
    {% endif %}
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    ]
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve),
    ]
    # debug toolbar
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
