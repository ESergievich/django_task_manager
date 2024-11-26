from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect


class UserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not authorized! Please log in.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class SelfActionOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, self.action_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class AuthorActionOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, self.action_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class SuccessMessageMixin:
    def form_valid(self, form):
        messages.success(self.request, _(self.success_message))
        return super().form_valid(form)


class RestrictDeleteIfLinkedToTaskMixin:
    def post(self, request, *args, **kwargs):
        if getattr(self.get_object(), self.related_name).exists():
            messages.error(self.request, _(self.restrict_message))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
