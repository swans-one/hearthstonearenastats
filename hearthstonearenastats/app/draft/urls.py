from django.conf.urls import patterns, url

from hearthstonearenastats.app.draft import views as draft_views


urlpatterns = patterns(
    '',
    url(r'^new/$', draft_views.DraftCreateView.as_view(), name='new-draft'),
    url(
        r'^(?P<draft_id>[0-9]+)/pick/(?P<pick_number>[0-9]+)/$',
        draft_views.DraftPickCreate.as_view(),
        name='draft-pick'
    ),
    url(
        r'^(?P<draft_id>[0-9]+)/game/(?P<game_number>[0-9]+)/$',
        draft_views.DraftGameCreate.as_view(),
        name='draft-game'
    ),
    url(
        r'^(?P<draft_id>[0-9]+)/prizes/$',
        draft_views.DraftPrizesCreate.as_view(),
        name='draft-prizes'
    )
)
