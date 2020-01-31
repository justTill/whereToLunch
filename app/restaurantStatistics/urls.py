from django.conf.urls import url
from .views import ChoicesChart, VotesChart

app_name = 'restaurantStatistics'

urlpatterns = [
    url(r'^api/charts/choices/$', ChoicesChart.as_view(), name='api-charts-choices'),
    url(r'^api/charts/votes/$', VotesChart.as_view(), name='api-charts-votes'),
]
