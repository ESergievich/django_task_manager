from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=False)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL,
                               verbose_name=_("Author"),
                               null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date of creation"))

    def __str__(self):
        return self.name
