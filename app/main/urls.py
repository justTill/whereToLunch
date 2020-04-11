from django.conf.urls import url
from django.urls import path
from .view.views import views as views
from .view.views import ChoicesChart, VotesChart

app_name = 'whereToLunch'

urlpatterns = [
    url(r'^absence$', views.absenceIndex, name='absenceIndex'),
    url(r'^save_new_absence$', views.save_new_absence, name='save_new_absence'),
    url(r'^delete_absences$', views.delete_absences, name='delete_absences'),

    url(r'^api/charts/choices/$', ChoicesChart.as_view(), name='api-charts-choices'),
    url(r'^api/charts/votes/$', VotesChart.as_view(), name='api-charts-votes'),

    path('', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('iAmOut/', views.iAmOut, name='iAmOut'),
    path('doNotCare/', views.doNotCare, name='doNotCare'),
]
