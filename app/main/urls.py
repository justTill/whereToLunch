from django.conf.urls import url
from django.urls import path
from .view.views import homepage, absenceIndex, ChoicesChart, VotesChart

app_name = 'main'

urlpatterns = [
    url(r'^absence$', absenceIndex.index, name='absenceIndex'),
    url(r'^save_new_absence$', absenceIndex.save_new_absence, name='save_new_absence'),
    url(r'^delete_absences$', absenceIndex.delete_absences, name='delete_absences'),

    url(r'^api/charts/choices/$', ChoicesChart.as_view(), name='api-charts-choices'),
    url(r'^api/charts/votes/$', VotesChart.as_view(), name='api-charts-votes'),

    path('', homepage.index, name='index'),
    path('vote/', homepage.vote, name='vote'),
    path('iAmOut/', homepage.iAmOut, name='iAmOut'),
    path('doNotCare/', homepage.doNotCare, name='doNotCare'),
]
