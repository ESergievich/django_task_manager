from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .models import Label
from utils import UserRequiredMixin, SuccessMessageMixin, RestrictDeleteIfLinkedToTaskMixin


class LabelsListView(UserRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_show.html'
    extra_context = {'title': _('Labels'), 'button': _('Create label')}
    context_object_name = 'labels'


class LabelCreateView(UserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ('name',)
    template_name = 'form.html'
    extra_context = {'title': _('Create label'), 'button': _('Create')}
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelUpdateView(UserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ('name',)
    template_name = 'form.html'
    extra_context = {'title': _('Update label'), 'button': _('Update')}
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully updated')


class LabelDeleteView(UserRequiredMixin, RestrictDeleteIfLinkedToTaskMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'form_delete.html'
    extra_context = {'title': _('Delete label'), 'button': _('Yes, delete')}
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')
    restrict_message = _('It`s not possible to delete the label that is being used')
    related_name = 'tasks_with_label'
