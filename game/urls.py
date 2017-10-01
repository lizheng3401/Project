from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'game'

urlpatterns=[
    url(r'^portfolio.html$', views.portfllio, name='portfolio'),
    url(r'^game/(?P<pk>[0-9]+)', views.gameInfo, name='gameInfo'),
    url(r'^download/game/(?P<pk>[0-9]+)', views.downloadGame, name='downloadGame'),
    url(r'^upload/game/$', views.uploadGame, name='uploadGame'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)