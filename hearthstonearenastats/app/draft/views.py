from braces.views import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic import CreateView
from django.views.generic.edit import FormView

from hearthstonearenastats.app.draft.models import (
    Draft, DraftPick, Game, Prizes
)
from hearthstonearenastats.app.draft.forms import DraftPickForm, PrizesForm


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
        return '/draft/{draft_id}/pick/1/'.format(draft_id=draft_id)


class DraftPickCreate(LoginRequiredMixin, FormView):
    form_class = DraftPickForm
    template_name = 'draft/pick_form.html'

    def get_form_kwargs(self):
        form_kwargs = super(DraftPickCreate, self).get_form_kwargs()
        form_kwargs['draft_id'] = self.kwargs['draft_id']
        return form_kwargs

    def get_context_data(self, **kwargs):
        kwargs = super(DraftPickCreate, self).get_context_data(**kwargs)
        kwargs.update(self.kwargs)
        return kwargs

    def dispatch(self, *args, **kwargs):
        draft = Draft.objects.get(pk=self.kwargs['draft_id'])
        if draft.user != self.request.user:
            raise Http404
        return super(DraftPickCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        choice_mapping = {
            'card1': form.cleaned_data['choice_1'],
            'card2': form.cleaned_data['choice_1'],
            'card3': form.cleaned_data['choice_1'],
        }
        pick = DraftPick(
            draft=Draft.objects.get(pk=self.kwargs['draft_id']),
            pick_number=int(self.kwargs['pick_number']),
            first=form.cleaned_data['choice_1'],
            second=form.cleaned_data['choice_1'],
            third=form.cleaned_data['choice_1'],
            choice=choice_mapping[form.cleaned_data['choosen']],
        )
        pick.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        draft_id = self.kwargs['draft_id']
        next_pick = int(self.kwargs['pick_number']) + 1
        if next_pick > 30:
            return '/draft/{draft_id}/game/1/'.format(draft_id=draft_id)
        else:
            url = '/draft/{draft_id}/pick/{next_pick}/'
            return url.format(draft_id=draft_id, next_pick=next_pick)


class DraftGameCreate(LoginRequiredMixin, CreateView):
    model = Game
    fields = ('opponent_hero', 'won', 'coin', 'mulligan_count')

    def dispatch(self, *args, **kwargs):
        draft = Draft.objects.get(pk=self.kwargs['draft_id'])
        if draft.user != self.request.user:
            raise Http404
        return super(DraftGameCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        game = form.save(commit=False)
        game.draft = Draft.objects.get(pk=self.kwargs['draft_id'])
        game.game_number = int(self.kwargs['game_number'])
        game.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs = super(DraftGameCreate, self).get_context_data(**kwargs)
        kwargs.update(self.kwargs)
        return kwargs

    def get_success_url(self):
        draft_id = self.kwargs['draft_id']
        next_game = int(self.kwargs['game_number']) + 1
        wins = Game.objects.filter(draft_id=draft_id, won=True).count()
        losses = Game.objects.filter(draft_id=draft_id, won=False).count()
        if next_game > 14 or wins == 12 or losses == 3:
            return '/draft/{draft_id}/prizes/'.format(draft_id=draft_id)
        else:
            url = '/draft/{draft_id}/game/{next_game}/'
            return url.format(draft_id=draft_id, next_game=next_game)


class DraftPrizesCreate(LoginRequiredMixin, FormView):
    form_class = PrizesForm
    template_name = 'draft/prizes_form.html'

    def dispatch(self, *args, **kwargs):
        draft = Draft.objects.get(pk=self.kwargs['draft_id'])
        if draft.user != self.request.user:
            raise Http404
        return super(DraftPrizesCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(DraftPrizesCreate, self).get_context_data(**kwargs)
        kwargs.update(self.kwargs)
        return kwargs

    def form_valid(self, form):
        card_fields = ['card_1', 'card_2', 'card_3']
        golden_fields = ['golden_card_1', 'golden_card_2', 'golden_card_3']
        prize_cards = [form.cleaned_data[c] for c in card_fields]
        prize_golden_cards = [form.cleaned_data[c] for c in golden_fields]
        prizes = Prizes(
            draft=Draft.objects.get(pk=self.kwargs['draft_id']),
            number_packs=form.cleaned_data['number_packs'],
            gold=form.cleaned_data['gold'],
        )
        prizes.save()
        for card in prize_cards:
            if card is not None:
                prizes.cards.add(card)
        for gold_card in prize_golden_cards:
            if gold_card is not None:
                prizes.golden_cards.add(gold_card)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        draft_id = self.kwargs['draft_id']
        return '/draft/{draft_id}/summary/'.format(draft_id=draft_id)
