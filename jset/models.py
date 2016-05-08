from django.db import models


class TmplVal(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.TextField(null=True, blank=True)
    cdt = models.DateTimeField(auto_now=True, null=True)
    udt = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name