from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext as _
from django_filters.views import FilterView

from .models import Task
from .forms import TaskCreateForm
from .filters import TaskFilter


class TasksRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class TasksListView(TasksRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks_show.html'
    filterset_class = TaskFilter
    extra_context = {
        'title': _('Tasks'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.filterset.qs
        context['button'] = _('Show')
        context['button_create'] = _('Create task')
        return context


class TaskCreateView(TasksRequiredMixin, CreateView):
    form_class = TaskCreateForm
    template_name = 'tasks/task_form.html'
    extra_context = {'title': _('Create task')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Create')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Task successfully created'))
        return reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(TasksRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_show.html"
    extra_context = {'title': _('Task view')}


class TaskUpdateView(TasksRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/task_form.html'
    extra_context = {'title': _('Update task')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Update')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Task successfully updated'))
        return reverse_lazy('tasks')


class TaskDeleteView(TasksRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    extra_context = {'title': _('Delete task')}
    template_name = 'tasks/task_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Yes, delete')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Task successfully deleted'))
        return reverse_lazy('tasks')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request,
                       _("You cannot delete this task because you are not the creator."))
        return redirect(reverse_lazy('tasks'))
