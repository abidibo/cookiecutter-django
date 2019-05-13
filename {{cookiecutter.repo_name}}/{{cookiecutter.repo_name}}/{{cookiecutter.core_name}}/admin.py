from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from constance import config

from .models import User


class ArchivedModelAdmin(admin.ModelAdmin):
    """ Utility class to filter out archived records """
    def get_queryset(self, request):
        qs = super(ArchivedModelAdmin, self).get_queryset(request)
        if config.HIDE_ARCHIVED:
            qs = qs.exclude(status=self.model.ARCHIVED)
        return qs


# register the user admin
admin.site.register(User, UserAdmin)
