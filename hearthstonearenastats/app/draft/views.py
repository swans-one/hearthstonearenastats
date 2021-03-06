from datetime import datetime

from braces.views import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from hearthstonearenastats.app.draft.forms import (
    DraftForm, DraftPickForm, PrizesForm
)
from hearthstonearenastats.app.draft.mixins import DraftStatusData
from hearthstonearenastats.app.draft.models import (
    DraftStatus, Draft, DraftPick, Game, Prizes
)


class DraftCreateView(LoginRequiredMixin, DraftStatusData, FormView):
    form_class = DraftForm
    template_name = 'draft/draft_form.html'

    def form_valid(self, form):
        # Clean up the form data and save a draft object
        hero_choice_mapping = {
            'hero1': form.cleaned_data['hero_1'],
            'hero2': form.cleaned_data['hero_2'],
            'hero3': form.cleaned_data['hero_3'],
        }
        self.draft = Draft.objects.create(
            user=self.request.user,
            first_hero=form.cleaned_data['hero_1'],
            second_hero=form.cleaned_data['hero_2'],
            third_hero=form.cleaned_data['hero_3'],
            hero_choice=hero_choice_mapping[form.cleaned_data['choosen']],
            start_date=datetime.utcnow(),
        )

        # Update draft_status
        draft_status, created = DraftStatus.objects.get_or_create(
            user=self.request.user
        )
        draft_status.draft = self.draft
        draft_status.stage = 'pick'
        draft_status.number = 1
        draft_status.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DraftCreateView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def get_success_url(self):
        draft_id = self.draft.id
        return '/draft/{draft_id}/pick/1/'.format(draft_id=draft_id)


class DraftPickCreate(LoginRequiredMixin, DraftStatusData, FormView):
    form_class = DraftPickForm
    template_name = 'draft/pick_form.html'

    def get_form_kwargs(self):
        form_kwargs = super(DraftPickCreate, self).get_form_kwargs()
        form_kwargs['draft_id'] = self.kwargs['draft_id']
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(DraftPickCreate, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        draft = Draft.objects.get(pk=self.kwargs['draft_id'])
        if draft.user != self.request.user:
            raise Http404
        return super(DraftPickCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # Clean up the form data and save a DraftPick object
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

        # Update the DraftStatus
        draft_status = DraftStatus.objects.get(user=self.request.user)
        next_pick = int(self.kwargs['pick_number']) + 1
        if next_pick > 30:
            draft_status.stage = 'game'
            draft_status.number = 1
        else:
            draft_status.stage = 'pick'
            draft_status.number = next_pick
        draft_status.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        draft_id = self.kwargs['draft_id']
        next_pick = int(self.kwargs['pick_number']) + 1
        if next_pick > 30:
            return '/draft/{draft_id}/game/1/'.format(draft_id=draft_id)
        else:
            url = '/draft/{draft_id}/pick/{next_pick}/'
            return url.format(draft_id=draft_id, next_pick=next_pick)


class DraftGameCreate(LoginRequiredMixin, DraftStatusData, CreateView):
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

        # Update the DraftStatus
        draft_status = DraftStatus.objects.get(user=self.request.user)
        draft_id = self.kwargs['draft_id']
        next_game = int(self.kwargs['game_number']) + 1
        wins = Game.objects.filter(draft_id=draft_id, won=True).count()
        losses = Game.objects.filter(draft_id=draft_id, won=False).count()
        if next_game > 14 or wins == 12 or losses == 3:
            draft_status.stage = 'prizes'
            draft_status.number = None
        else:
            draft_status.stage = 'game'
            draft_status.number = next_game
        draft_status.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DraftGameCreate, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

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


class DraftPrizesCreate(LoginRequiredMixin, DraftStatusData, FormView):
    form_class = PrizesForm
    template_name = 'draft/prizes_form.html'

    def dispatch(self, *args, **kwargs):
        draft = Draft.objects.get(pk=self.kwargs['draft_id'])
        if draft.user != self.request.user:
            raise Http404
        return super(DraftPrizesCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DraftPrizesCreate, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def form_valid(self, form):
        card_fields = ['card_1', 'card_2', 'card_3']
        golden_fields = ['golden_card_1', 'golden_card_2', 'golden_card_3']
        prize_cards = [form.cleaned_data[c] for c in card_fields]
        prize_golden_cards = [form.cleaned_data[c] for c in golden_fields]

        # Create the base prizes object.
        prizes = Prizes(
            draft=Draft.objects.get(pk=self.kwargs['draft_id']),
            number_packs=form.cleaned_data['number_packs'],
            gold=form.cleaned_data['gold'],
            dust=form.cleaned_data['dust'],
        )
        prizes.save()

        # Add the cards in the many to many relationship.
        for card in prize_cards:
            if card is not None:
                prizes.cards.add(card)
        for gold_card in prize_golden_cards:
            if gold_card is not None:
                prizes.golden_cards.add(gold_card)

        # Update the DraftStatus
        draft_status = DraftStatus.objects.get(user=self.request.user)
        draft_status.draft = None
        draft_status.stage = None
        draft_status.number = None
        draft_status.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        draft_id = self.kwargs['draft_id']
        return '/draft/{draft_id}/summary/'.format(draft_id=draft_id)


class DraftSummary(LoginRequiredMixin, TemplateView):
    template_name = 'draft/summary.html'

    def get_context_data(self, **kwargs):
        kwargs = super(DraftSummary, self).get_context_data(**kwargs)
        kwargs['draft'] = Draft.objects.get(pk=self.kwargs['draft_id'])
        return kwargs
