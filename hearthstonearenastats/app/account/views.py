from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class ProfileMainPage(LoginRequiredMixin, TemplateView):
    template_name = 'account/home.html'

    login_url = reverse_lazy('login')

    def get_context_data(self):
        pass


class ProfileEdit(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    login_url = reverse_lazy('login')

    def get_context_data(self):
        pass
