from django.conf.urls import url
from .views import ChoicesChart, VotesChart

app_name = 'restaurantStatistics'

urlpatterns = [
    url(r'^api/chart/choices/$', ChoicesChart.as_view(), name='api-chart-choices'),
    url(r'^api/chart/votes/$', VotesChart.as_view(), name='api-chart-votes'),
]
