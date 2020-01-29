from django.conf.urls import url
from absenceCalendar import views as views

app_name = 'absenceCalendar'

urlpatterns = [
    url(r'^absence$', views.absenceIndex, name='absenceIndex'),
    url(r'^save_new_absence$', views.save_new_absence, name='save_new_absence'),
    url(r'^delete_absences$', views.delete_absences, name='delete_absences'),
]
