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
)
