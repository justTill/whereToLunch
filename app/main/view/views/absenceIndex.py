import structlog
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.conf import settings
from main.controller.logic import weather_context, AbsenceLogic, VoteLogic, CustomizeLogic
from main.controller.forms import AbsenceForm
from utils.enum import Reasons
from utils.date import dateManager

logger = structlog.getLogger(__name__)

absence_logic = AbsenceLogic()
vote_logic = VoteLogic()
customize_logic = CustomizeLogic()


def index(request):
    template = loader.get_template('templates/absenceIndex.html')
    context = get_standard_context()
    return HttpResponse(template.render(context, request))


@staff_member_required
def save_new_absence(request):
    logger.debug("save absence")
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
            logger.info("form is valid, save absence %s for user: %s and delete old one" %(new_absence, request.user.username))
            if new_absence.absenceFrom <= dateManager.current_vote_day():
                logger.debug("User voted, we need to delete that votes")
                vote_logic.delete_votes_from_user(request.user)
            return HttpResponseRedirect(reverse('main:absenceIndex'))
        else:
            logger.warn("Form was not valid")
            context['absence_form'] = form
    return render(request, 'templates/absenceIndex.html', context)


@staff_member_required
def delete_absences(request):
    user = request.user
    absences = request.POST.getlist('absenceBox')
    absence_logic.delete_absences_for_user(user, absences)
    logger.info("delete absences: %s for user %s" % (user.username, absences))
    return HttpResponseRedirect(reverse('main:absenceIndex'))


def get_standard_context():
    logger.debug("get standard context things for Absences index page")
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
