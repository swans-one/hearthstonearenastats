from django.conf.urls import patterns, url

from hearthstonearenastats.app.draft import views as draft_views


urlpatterns = patterns(
    '',
    url(r'^new/$', draft_views.DraftCreateView.as_view()),
)
