from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='logout'),

    url(r'^account/',
        include('hearthstonearenastats.app.account.urls',
                namespace='account')),
    url(r'^account/profile/',
        TemplateView.as_view(template_name='account/profile.html'))
)
