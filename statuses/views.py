from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from .models import Status
from .forms import StatusCreateForm


class StatusesRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class StatusesListView(StatusesRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_show.html'
    extra_context = {'title': _('Statuses')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = self.model.objects.all()
        context['button'] = _('Create status')
        return context


class StatusCreateView(StatusesRequiredMixin, CreateView):
    form_class = StatusCreateForm
    template_name = 'statuses/status_form.html'
    extra_context = {'title': _('Create status')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Create')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status successfully created'))
        return reverse_lazy('statuses')


class StatusUpdateView(StatusesRequiredMixin, UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/status_form.html'
    extra_context = {'title': _('Update status')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Update')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status successfully updated'))
        return reverse_lazy('statuses')


class StatusDeleteView(StatusesRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    extra_context = {'title': _('Delete status')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Yes, delete')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status successfully deleted'))
        return reverse_lazy('statuses')

    def post(self, request, *args, **kwargs):
        if self.get_object().statuses.count():
            messages.error(
                self.request,
                _('It`s not possible to delete the status that is being used')
            )
            return redirect('statuses')
        return super().post(request, *args, **kwargs)
