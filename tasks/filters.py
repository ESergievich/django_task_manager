from django.contrib.auth import get_user_model
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django import forms
from django.utils.translation import gettext_lazy as _

from statuses.models import Status
from labels.models import Label


class TaskFilter(FilterSet):

    statuses = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status')
    )

    executors = ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        label=_('Executor')
    )

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    own_tasks = BooleanFilter(
        label=_('Only own tasks'),
        widget=forms.CheckboxInput,
        method='get_own_tasks',
    )

    def get_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset
