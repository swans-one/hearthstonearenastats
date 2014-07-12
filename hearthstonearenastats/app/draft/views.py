from braces.views import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from hearthstonearenastats.app.draft.models import Draft


class DraftCreateView(LoginRequiredMixin, CreateView):
    model = Draft
    fields = ('first_hero', 'second_hero', 'third_hero', 'hero_choice')

    def form_valid(self, form):
        """If the form is valid, this method is called to save and redirect.

        Since we do not have a separate form (One is created from our
        model/fields combination, we do the extra logic of adding data
        based on the user here.
        """
        self.draft = form.save(commit=False)
        self.draft.user = self.request.user
        self.draft.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        draft_id = self.draft.id
        return '/draft/{draft_id}/pick/1'.format(draft_id=draft_id)
