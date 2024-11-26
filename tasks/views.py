from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from .models import Task
from .filters import TaskFilter
from utils import UserRequiredMixin, SuccessMessageMixin, AuthorActionOnlyMixin


class TasksListView(UserRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks_show.html'
    filterset_class = TaskFilter
    extra_context = {
        'title': _('Tasks'),
        'button': _('Show'),
        'button_create': _('Create task')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.filterset.qs
        return context


class TaskCreateView(UserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ('name', 'description', 'executor', 'labels', 'status')
    template_name = 'form.html'
    extra_context = {'title': _('Create task'), 'button': _('Create')}
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(UserRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_show.html"
    extra_context = {'title': _('Task view')}


class TaskUpdateView(UserRequiredMixin, AuthorActionOnlyMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ('name', 'description', 'executor', 'labels', 'status')
    template_name = 'form.html'
    extra_context = {'title': _('Update task'), 'button': _('Update')}
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')
    action_message = _("You cannot update this task because you are not the creator.")


class TaskDeleteView(UserRequiredMixin, AuthorActionOnlyMixin, SuccessMessageMixin, DeleteView):
    model = Task
    extra_context = {'title': _('Delete task'), 'button': _('Yes, delete')}
    template_name = 'form_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    action_message = _("You cannot delete this task because you are not the creator.")
