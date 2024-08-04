from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from statuses.models import Status
from labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=False)
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="statuses",
                               blank=False, verbose_name=_("Status"))
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                               related_name="authors", verbose_name=_("Author"))
    executor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 related_name="executors", verbose_name=_("Executor"))
    labels = models.ManyToManyField(Label, through='TaskLabelRelation',
                                    through_fields=('task', 'label'),
                                    related_name="labels", verbose_name=_("Labels"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date of creation"))

    class TaskLabelRelation(models.Model):
        task = models.ForeignKey('Task', on_delete=models.CASCADE)
        label = models.ForeignKey(Label, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
