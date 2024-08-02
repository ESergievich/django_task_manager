from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .forms import RegisterUserForm


class ListUsers(ListView):
    model = get_user_model()
    template_name = 'users/show_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.model.objects.all()
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/user_form.html'
    extra_context = {'title': 'Регистрация',
                     'button': 'Сохранить'}

    def get_success_url(self):
        return reverse_lazy('login')


class ChangeUser:
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if request.user.pk != pk:
            messages.error(request, 'У вас нет доступа к asdasd странице.')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UpdateUser(ChangeUser, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_form.html'
    extra_context = {'title': 'Регистрация',
                     'button': 'Изменить'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users')


class DeleteUser(ChangeUser, LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/user_form.html'
    extra_context = {'title': 'Удаление пользователя',
                     'button': 'Да, удалить'}

    def get_object(self, queryset=None):
        print(self)
        print(self.request)
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users')
