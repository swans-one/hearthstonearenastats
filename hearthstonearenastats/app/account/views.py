from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin

class ProfileMainPage(LoginRequiredMixin, TemplateView):
    template_name = 'account/account-home.html'

    login_url = '/account/login/'

    def get_context_data(self):
        pass
