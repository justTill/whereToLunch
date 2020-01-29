from django.urls import path
from polls import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('iAmOut/', views.iAmOut, name='iAmOut'),
    path('doNotCare/', views.doNotCare, name='doNotCare'),
]
