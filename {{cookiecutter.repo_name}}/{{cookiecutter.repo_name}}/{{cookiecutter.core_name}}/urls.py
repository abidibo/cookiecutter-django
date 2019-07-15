"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.urls import path, re_path
{% if cookiecutter.admin == 'django-baton' %}
from baton.autodiscover import admin
{% else %}
from django.contrib import admin
{% endif %}
from django.conf import settings
from django.views.generic import TemplateView
from django.views import static
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    {% if cookiecutter.admin == 'django-baton' %}
    path('baton/', include('baton.urls')),
    {% endif %}
    re_path(r'^$', TemplateView.as_view(template_name='home.html'),
            name='home'),
    # ckeditor uploader
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # treenav
    path('treenav/', include('treenav.urls')),
    {% if cookiecutter.use_filer == 'y' %}
    # filer
    path('filer/', include('filer.urls')),
    {% endif %}
    {% if cookiecutter.admin == 'django-grappelli' %}
    # grappelli
    path('grappelli/', include('grappelli.urls')),
    {% endif %}
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$',
                static.serve,
                {'document_root': settings.MEDIA_ROOT}),
    ]
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve),
    ]
    # debug toolbar
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
