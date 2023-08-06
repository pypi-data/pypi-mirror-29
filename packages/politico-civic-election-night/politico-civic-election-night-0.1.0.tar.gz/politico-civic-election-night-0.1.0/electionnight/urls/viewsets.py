from django.urls import path, re_path

from electionnight.viewsets import (BodyDetail, BodyList, ElectionDayDetail,
                                    ElectionDayList, OfficeDetail, OfficeList,
                                    SpecialDetail, SpecialList, StateDetail,
                                    StateList)

urlpatterns = [
    path(
        'api/elections/',
        ElectionDayList.as_view(),
        name='electionnight_api_election-list',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/$',
        ElectionDayDetail.as_view(),
        name='electionnight_api_election-detail',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/states/$',
        StateList.as_view(),
        name='electionnight_api_state-election-list',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/states/(?P<pk>.+)/$',
        StateDetail.as_view(),
        name='electionnight_api_state-election-detail',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/special-elections/$',
        SpecialList.as_view(),
        name='electionnight_api_special-election-list',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})'
        r'/special-elections/(?P<pk>.+)/$',
        SpecialDetail.as_view(),
        name='electionnight_api_special-election-detail',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/bodies/$',
        BodyList.as_view(),
        name='electionnight_api_body-election-list',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/bodies/(?P<pk>.+)/$',
        BodyDetail.as_view(),
        name='electionnight_api_body-election-detail',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/executive-offices/$',
        OfficeList.as_view(),
        name='electionnight_api_office-election-list',
    ),
    re_path(
        r'^api/elections/(?P<date>\d{4}-\d{2}-\d{2})/'
        r'executive-offices/(?P<pk>.+)/$',
        OfficeDetail.as_view(),
        name='electionnight_api_office-election-detail',
    ),
]
