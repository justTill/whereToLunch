from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from weather.logic import weather_context
from absenceCalendar.forms import AbsenceForm
from absenceCalendar.logic import AbsenceLogic
from utils.enum import Reasons
from utils.date import dateManager
from polls.logic import VoteLogic
from django.conf import settings
from utils.customize.logic import CustomizeLogic

absence_logic = AbsenceLogic()
vote_logic = VoteLogic()
customize_logic = CustomizeLogic()

today = dateManager.today()
tomorrow = dateManager.tomorrow()
current_vote_day = dateManager.current_vote_day()


def absenceIndex(request):
    template = loader.get_template('absenceCalendar/absenceIndex.html')
    context = get_standard_context()
    return HttpResponse(template.render(context, request))


@staff_member_required
def save_new_absence(request):
    context = get_standard_context()
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.clean()
            new_absence = form.save(commit=False)
            new_absence.user = request.user
            new_absence.reason = Reasons.ABSENT.value
            new_absence.save()
            absence_logic.delete_vote_absence_for_user(request.user, new_absence.absenceFrom)
            if new_absence.absenceFrom <= current_vote_day:
                vote_logic.delete_votes_from_user(request.user)
            return HttpResponseRedirect(reverse('absenceCalendar:absenceIndex'))
        else:
            context['absence_form'] = form
    return render(request, 'absenceCalendar/absenceIndex.html', context)


@staff_member_required
def delete_absences(request):
    user = request.user
    absences = request.POST.getlist('absenceBox')
    absence_logic.delete_absences_for_user(user, absences)
    return HttpResponseRedirect(reverse('absenceCalendar:absenceIndex'))


def get_standard_context():
    absences_from_users = absence_logic.get_sorted_absent_absences()
    website_name = customize_logic.get_website_name()
    background_image_url = customize_logic.get_background_image_url()
    return {
        'weather_context': weather_context(),
        'absence_form': AbsenceForm(),
        'is_after_noon': dateManager.is_after_noon(),
        'absences_from_users': absences_from_users,
        'website_name': website_name,
        'background_image_url': background_image_url,
        'django_static_url': settings.STATIC_URL,
    }
