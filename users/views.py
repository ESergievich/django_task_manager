from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .forms import RegisterUserForm, LoginUserForm
from utils import SuccessMessageMixin, UserRequiredMixin, SelfActionOnlyMixin


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {'title': _("Log In"), 'button': _("Enter")}
    success_url = reverse_lazy('home')
    success_message = _('You are logged in')


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, _('You are logged out'))
        return redirect('home')


class UsersListView(ListView):
    model = get_user_model()
    template_name = 'users/users_show.html'
    extra_context = {'title': _('Users')}
    context_object_name = 'users'


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'form.html'
    extra_context = {'title': _('Registration'), 'button': _('Register')}
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')


class UserUpdateView(UserRequiredMixin, SelfActionOnlyMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'form.html'
    extra_context = {'title': _('Update user'), 'button': _('Update')}
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated')
    action_message = _('You cannot update another user\'s account.')


class UserDeleteView(UserRequiredMixin, SelfActionOnlyMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'form_delete.html'
    extra_context = {'title': _('Delete user'), 'button': _('Yes, delete')}
    success_url = reverse_lazy('users')
    success_message = _('User is successfully deleted')
    action_message = _('You cannot delete another user\'s account.')
