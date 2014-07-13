from django import forms

from hearthstonearenastats.app.draft.models import Draft
from hearthstonearenastats.app.card.models import Card


CHOICES = (
    ('card1', 'Card 1'),
    ('card2', 'Card 2'),
    ('card3', 'Card 3'),
)


class DraftPickForm(forms.Form):
    # Set the initial querysets to none. They will be populated
    # during `__init__`
    choice_1 = forms.ModelChoiceField(queryset=Card.objects.none())
    choice_2 = forms.ModelChoiceField(queryset=Card.objects.none())
    choice_3 = forms.ModelChoiceField(queryset=Card.objects.none())
    choosen = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        draft_id = kwargs.pop('draft_id')
        super(DraftPickForm, self).__init__(*args, **kwargs)
        card_qs = get_card_qs(draft_id)
        self.fields['choice_1'].queryset = card_qs
        self.fields['choice_2'].queryset = card_qs
        self.fields['choice_3'].queryset = card_qs


def get_card_qs(draft_id):
    draft = Draft.objects.get(pk=draft_id)
    hero = draft.hero_choice
    qs = Card.current_patch.filter(
        hero__in=(hero, 'neutral'),
        collectible=True,
    ).order_by('mana', 'name')
    return qs
