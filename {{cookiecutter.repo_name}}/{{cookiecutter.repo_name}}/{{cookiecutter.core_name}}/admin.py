from django.contrib import admin

from constance import config


class ArchivedModelAdmin(admin.ModelAdmin):
    """ Utility class to filter out archived records """
    def get_queryset(self, request):
        qs = super(ArchivedModelAdmin, self).get_queryset(request)
        if config.HIDE_ARCHIVED:
            qs = qs.exclude(status=self.model.ARCHIVED)
        return qs
