from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from .models import Label
from .forms import LabelCreateForm


class LabelsRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class LabelsListView(LabelsRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_show.html'
    extra_context = {'title': _('Labels')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = self.model.objects.all()
        context['button'] = _('Create label')
        return context


class LabelCreateView(LabelsRequiredMixin, CreateView):
    form_class = LabelCreateForm
    template_name = 'labels/label_form.html'
    extra_context = {'title': _('Create label')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Create')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label successfully created'))
        return reverse_lazy('labels')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelUpdateView(LabelsRequiredMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/label_form.html'
    extra_context = {'title': _('Update label')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Update')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label successfully updated'))
        return reverse_lazy('labels')


class LabelDeleteView(LabelsRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    extra_context = {'title': _('Delete label')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Yes, delete')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label successfully deleted'))
        return reverse_lazy('labels')

    def post(self, request, *args, **kwargs):
        if self.get_object().labels.count():
            messages.error(
                self.request,
                _('It`s not possible to delete the label that is being used')
            )
            return redirect('labels')
        return super().post(request, *args, **kwargs)
