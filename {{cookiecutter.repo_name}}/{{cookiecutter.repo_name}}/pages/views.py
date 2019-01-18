{% raw %}from django.conf import settings
from .models import Page
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect

DEFAULT_TEMPLATE = 'pages/default.html'

# This view is called from PageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching page exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.


def page(request, url):
    """
    Public interface to the page view.

    Models: `pages.page`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`pages/default.html` if template_name is not defined.
    Context:
        page
            `pages.page` object
    """
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        p = get_object_or_404(Page, url=url, sites=site_id)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            p = get_object_or_404(Page, url=url, sites=site_id)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_page(request, p)


@csrf_protect
def render_page(request, p):
    """
    Internal interface to the page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if p.registration_required and not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    # If page is not pusblished, raise 404
    if not p.status == Page.PUBLISHED:
        raise Http404
    if p.template_name:
        template = loader.select_template((p.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    response = HttpResponse(template.render({'page': p}, request))
    return response
{% endraw %}
