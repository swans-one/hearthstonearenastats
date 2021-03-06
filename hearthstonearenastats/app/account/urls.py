from django.conf.urls import patterns, url

from hearthstonearenastats.app.account import views as account_views


urlpatterns = patterns(
    '',
    url(r'^home/$', account_views.ProfileMainPage.as_view(), name='home'),
    url(r'^profile/$', account_views.ProfileEdit.as_view(), name='profile'),
)
