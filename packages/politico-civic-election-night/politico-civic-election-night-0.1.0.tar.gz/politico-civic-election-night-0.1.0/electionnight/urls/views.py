from django.urls import path, re_path

from electionnight.views import DevHome, SpecialElectionPage, StatePage

urlpatterns = [
    path('', DevHome.as_view(), name='preview'),
    path(StatePage.path, StatePage.as_view(), name=StatePage.name),
    re_path(
        SpecialElectionPage.path,
        SpecialElectionPage.as_view(),
        name=SpecialElectionPage.name
    ),
]
