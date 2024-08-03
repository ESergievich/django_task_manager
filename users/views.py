from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from .forms import RegisterUserForm


class UsersListView(ListView):
    model = get_user_model()
    template_name = 'users/users_show.html'
    extra_context = {'title': _('Users')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.model.objects.all()
        return context


class UserRegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/user_form.html'
    extra_context = {'title': _('Register')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Create user')
        return context

    def get_success_url(self):
        messages.success(self.request, _('User is successfully registered'))
        return reverse_lazy('login')


class UserChangeView:
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if not request.user.is_active:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
        elif request.user.pk != pk:
            messages.error(request, _('You do not have permission to change another user.'))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UserChangeView, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_form.html'
    extra_context = {'title': _('Update user')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Update')
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, _('User is successfully updated'))
        return reverse_lazy('users')


class UserDeleteView(UserChangeView, LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/user_delete.html'
    extra_context = {'title': _('Delete user')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Yes, delete')
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, _('User is successfully deleted'))
        return reverse_lazy('users')
