from django.db import models


class PageManager(models.Manager):

    def published(self, **kwargs):
        return self.filter(status=2, **kwargs)
