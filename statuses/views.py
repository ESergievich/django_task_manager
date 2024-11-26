from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .models import Status
from utils import UserRequiredMixin, SuccessMessageMixin, RestrictDeleteIfLinkedToTaskMixin


class StatusesListView(UserRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_show.html'
    extra_context = {'title': _('Statuses'), 'button': _('Create status')}
    context_object_name = 'statuses'


class StatusCreateView(UserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ('name',)
    template_name = 'form.html'
    extra_context = {'title': _('Create status'), 'button': _('Create')}
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class StatusUpdateView(UserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ('name',)
    template_name = 'form.html'
    extra_context = {'title': _('Update status'), 'button': _('Update')}
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')


class StatusDeleteView(UserRequiredMixin, RestrictDeleteIfLinkedToTaskMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'form_delete.html'
    extra_context = {'title': _('Delete status'), 'button': _('Yes, delete')}
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    restrict_message = _('It`s not possible to delete the status that is being used')
    related_name = 'tasks_with_status'
