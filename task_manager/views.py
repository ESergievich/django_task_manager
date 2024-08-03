from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils.translation import gettext as _

from .forms import LoginUserForm


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {
        'title': _("Log In"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _("Enter")
        return context

    def get_success_url(self):
        messages.success(self.request, _('You are logged in'))
        return reverse_lazy('home')


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, _('You are logged out'))
        return redirect('home')
